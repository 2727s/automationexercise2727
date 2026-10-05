"""Shared Playwright fixtures. Tests run in Chromium only."""

import logging
import os
import shutil
import subprocess
from pathlib import Path

import allure
import pytest
from playwright.sync_api import BrowserContext, Page

# Screenshots and Allure files for each run.
INVENTORY = Path("artifacts") / "test inventory"
SCREENSHOTS = INVENTORY / "screenshots"
RESULTS_DIR = INVENTORY / "allure-results"
REPORT_DIR = Path("reports")
LOG_DIR = Path("logs")
# pytest opens logs/test_run.log during startup, so the folder must already exist.
LOG_DIR.mkdir(parents=True, exist_ok=True)
_log = logging.getLogger("tests")
_test_name = "-"


class _TestNameFilter(logging.Filter):
    """Put the current pytest test name on every log line."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.test_name = _test_name
        return True


# Filter this logger, not the root logger. Pytest writes the file from here.
_log.addFilter(_TestNameFilter())


def _set_test_name(name: str) -> None:
    global _test_name
    _test_name = name


# Hosts that inject banners over the storefront and slow page load.
_AD_HOSTS = (
    "googlesyndication.com",
    "doubleclick.net",
    "googleadservices.com",
    "adservice.google.com",
)


def _abort_ads(route) -> None:
    if any(host in route.request.url for host in _AD_HOSTS):
        route.abort()
        return
    route.continue_()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, base_url):
    """Desktop Chromium context pointed at the practice site."""
    return {
        **browser_context_args,
        "base_url": base_url,
        "viewport": {"width": 1280, "height": 800},
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot for every test and attach that same file to Allure."""
    outcome = yield
    report = outcome.get_result()
    # Log setup failures too. A broken test often never reaches the browser.
    _set_test_name(item.name)
    if report.when == "setup" and report.failed:
        _log.error("SETUP FAILED")
        return
    if report.when != "call":
        return
    _log.info(report.outcome.upper())
    page = item.funcargs.get("page")
    if page is None:
        return
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    safe_name = item.name.replace("[", "_").replace("]", "")
    path = SCREENSHOTS / f"{safe_name}.png"
    page.screenshot(path=str(path))
    allure.attach.file(
        str(path), name="screenshot", attachment_type=allure.attachment_type.PNG
    )


def pytest_collectreport(report):
    """A syntax error is found before the test runs. Still write it to the log."""
    if report.failed:
        _set_test_name(report.nodeid)
        _log.error("ERROR\n%s", report.longrepr)


def _allure_command() -> list[str] | None:
    """Find allure.bat from the local install, then from PATH."""
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "allure"
    installed = sorted(local.glob("allure-*/bin/allure.bat"))
    if installed:
        return [str(installed[-1])]
    found = shutil.which("allure")
    if found:
        return [found]
    return None


def pytest_sessionfinish(session, exitstatus):
    """After pytest, write the Allure page to reports/index.html."""
    if getattr(session.config.option, "collectonly", False) or not RESULTS_DIR.exists():
        return
    command = _allure_command()
    if command is None:
        print("Allure CLI not found, so reports/index.html was not created.")
        return
    env = os.environ.copy()
    java_home = Path(r"C:\Program Files\Eclipse Adoptium\jre-21.0.12.101-hotspot")
    if java_home.exists():
        env["JAVA_HOME"] = str(java_home)
        env["PATH"] = str(java_home / "bin") + os.pathsep + env.get("PATH", "")
    subprocess.run(
        [*command, "generate", str(RESULTS_DIR), "-o", str(REPORT_DIR), "--clean"],
        check=False,
        env=env,
    )


@pytest.fixture(autouse=True)
def _prepare_page(page: Page, context: BrowserContext):
    """Block ad requests and give the slow practice site a longer timeout."""
    context.route("**/*", _abort_ads)
    page.set_default_timeout(20_000)
    page.set_default_navigation_timeout(45_000)
    yield

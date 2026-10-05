# automationexercise2727

Playwright + pytest page-object suite for [Automation Exercise](https://www.automationexercise.com/). Browser: Chromium.

## Setup

```powershell
uv sync
uv run playwright install chromium
```

The HTML report also needs Java and the [Allure command line](https://allurereport.org/docs/v2/install-for-windows/). On this machine they are already installed:

- Java: `C:\Program Files\Eclipse Adoptium\jre-21.0.12.101-hotspot`
- Allure: `C:\Users\pione\AppData\Local\allure\allure-2.46.1\bin`

Open a new terminal after installing them so `allure` is on `PATH`.

## Run

```powershell
uv run pytest
```

Pytest only accepts test paths. `uv run pytest open reports/index.html` fails because it looks for a folder named `open`.

## Report

After the run, pytest writes:

| Path | Contents |
| --- | --- |
| `reports/index.html` | Allure HTML report |
| `artifacts/test inventory/screenshots/` | One screenshot per test |
| `artifacts/test inventory/allure-results/` | Raw Allure results |
| `logs/test_run.log` | Pass, fail, or collection error. The folder stays visible; each run replaces the file. |

`reports/index.html` loads files next to it, so opening that file directly stays blank. Open the report with:

```powershell
allure open reports
```

Or, from the project folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\cli.ps1
```

`cli.ps1` runs `allure serve allure-results`. Leave that window open while the report is in the browser.

## Login data

`.env` holds the login/password pair. The value `faker_letters` is replaced with random letters on every read. Login becomes an email such as `gpzztzkgrm@example.com`.

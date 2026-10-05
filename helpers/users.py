"""Read the login/password pair from .env and expand faker_letters."""

import os
from pathlib import Path

from dotenv import load_dotenv

from helper.faker_data import faker_letters

# Project root is the parent of this helpers folder.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# .env value that means "generate random letters".
FAKER_LETTERS = "faker_letters"


def get_login_password() -> tuple[str, str]:
    """Return the (login, password) pair.

    A value of faker_letters becomes a new random letter string.
    Login is an email so the site form will accept it.
    """
    return _resolve("LOGIN", email=True), _resolve("PASSWORD")


def _resolve(key: str, *, email: bool = False) -> str:
    raw = os.getenv(key, "").strip()
    if raw == FAKER_LETTERS:
        letters = faker_letters().lower()
        return f"{letters}@example.com" if email else letters
    if not raw:
        raise RuntimeError(f"Set {key} in .env")
    return raw

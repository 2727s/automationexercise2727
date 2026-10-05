"""Random letters, names, and postal codes."""

from faker import Faker

_fake = Faker()


def faker_letters(length: int = 10) -> str:
    """Return a string of random letters. No digits or symbols."""
    return "".join(_fake.random_letters(length=length))


def get_name() -> tuple[str, str]:
    """Return a random (first name, last name) pair."""
    return _fake.first_name(), _fake.last_name()


def get_postcode() -> str:
    """Return a random postal code."""
    return _fake.postcode()

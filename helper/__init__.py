"""Faker generators and the login pair used by tests."""

from helper.faker_data import faker_letters, get_name, get_postcode
from helper.users import get_login_password

__all__ = ["faker_letters", "get_login_password", "get_name", "get_postcode"]

import re

from src.auth.errors import PasswordValidationError, PhoneValidationError


def validate_password(password: str, confirm_password: str):
    if password != confirm_password:
        raise PasswordValidationError("Password and confirm_password do not match")
    if len(password) < 8:
        raise PasswordValidationError("Password is too short")
    if not any(c.isalpha() and c.isascii() for c in password):
        raise PasswordValidationError("Password must contain Latin characters")
    if not any(c.isupper() for c in password):
        raise PasswordValidationError(
            "Password must contain at least one uppercase letter"
        )
    if not any(c in "$%&!:." for c in password):
        raise PasswordValidationError("Password must contain at least one of $%&!:.")


def validate_phone(phone: str):
    phone_pattern = re.compile(r"^\+7\d{10}$")
    if not phone_pattern.match(phone):
        raise PhoneValidationError("Invalid phone number")

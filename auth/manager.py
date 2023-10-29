import re
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from auth.database import User, get_user_db
from auth.errors import PhoneValidationError, PasswordValidationError

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def __validate_password(self, password: str):
        if len(password) < 8:
            raise PasswordValidationError("Password is too short")
        if not any(c.isalpha() and c.isascii() for c in password):
            raise PasswordValidationError("Password must contain Latin characters")
        if not any(c.isupper() for c in password):
            raise PasswordValidationError("Password must contain at least one uppercase letter")
        if not any(c in '$%&!:.' for c in password):
            raise PasswordValidationError("Password must contain at least one of $%&!:.")

    def __validate_phone(self, phone: str):
        phone_pattern = re.compile(r'^\+7\d{10}$')
        if not phone_pattern.match(phone):
            raise PhoneValidationError("Invalid phone number")

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        self.__validate_password(password)
        self.__validate_phone(user_dict['phone_number'])
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

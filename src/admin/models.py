from sqladmin import ModelView

from auth.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    can_delete = False
    column_details_exclude_list = [User.hashed_password, ]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

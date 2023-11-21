from sqladmin import ModelView

from src.auth.models import User
from src.goods.models import Goods


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    can_delete = False
    column_details_exclude_list = [
        User.hashed_password,
    ]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class GoodsAdmin(ModelView, model=Goods):
    column_list = [c.name for c in Goods.__table__.c]
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-box"

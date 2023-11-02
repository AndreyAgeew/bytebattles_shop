from fastapi import Request, APIRouter, Depends

from fastapi.templating import Jinja2Templates

from auth.dependecies import get_current_user
from auth.models import User

router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request, user: User = Depends(get_current_user)):
    title = "Базовая страница"
    return templates.TemplateResponse("base.html", {"request": request, "title": title, "user": user})

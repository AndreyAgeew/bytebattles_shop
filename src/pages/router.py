from fastapi import Request, APIRouter, Depends, HTTPException

from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

from auth.base_config import fastapi_users
from auth.models import User

router = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request, user: User = Depends(fastapi_users.current_user())):
    title = "Базовая страница"
    return templates.TemplateResponse("base.html", {"request": request, "title": title, "user": user})



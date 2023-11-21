from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependecies import get_current_admin_user
from auth.models import User
from database import get_async_session
from goods.dao import GoodsDAO
from goods.models import Goods

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.post("/add_to_goods/{goods_id}/")
async def add_image_to_goods(
    goods_id: int,
    image: UploadFile,
    user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session),
):
    existing_goods = await GoodsDAO.find_by_id(session, goods_id)
    if existing_goods is None:
        raise HTTPException(status_code=404, detail="Товар не найден")

    with open(f"src/static/img/goods/{image.filename}", "wb") as f:
        f.write(image.file.read())

    # Обновите поле image_url товара в базе данных, используя ваш новый метод
    image_url = f"/static/img/goods/{image.filename}"
    await GoodsDAO.update_goods_image(session, goods_id, image_url)
    await session.commit()

    return {"filename": image.filename}

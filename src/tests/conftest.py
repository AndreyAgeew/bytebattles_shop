import pytest
from src.database import Base, async_session_maker, engine

from src.auth.models import Role, User
from src.goods.models import Goods

@pytest.fixture
async def prepare_data_base(autouse=True):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)




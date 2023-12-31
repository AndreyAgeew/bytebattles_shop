"""Add image_url in goods

Revision ID: 81faf469dc9e
Revises: af5a34999f09
Create Date: 2023-11-04 23:43:36.271294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81faf469dc9e'
down_revision: Union[str, None] = 'af5a34999f09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goods', 'image_url')
    # ### end Alembic commands ###

"""Create Order

Revision ID: e05eb5fe95e7
Revises: 81faf469dc9e
Create Date: 2023-11-15 16:47:40.558902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e05eb5fe95e7'
down_revision: Union[str, None] = '81faf469dc9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('initiator_id', sa.Integer(), nullable=False),
                    sa.Column('basket_history', sa.JSON(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
                    sa.Column('status', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['initiator_id'], ['user.id'], ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    # ### end Alembic commands ###

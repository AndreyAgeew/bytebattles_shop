"""Add columns in user table

Revision ID: 5622d0f01bb9
Revises: 15d2b45e30b4
Create Date: 2023-10-29 11:44:57.210263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5622d0f01bb9'
down_revision: Union[str, None] = '15d2b45e30b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=320), nullable=False))
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.create_index(op.f('ix_user_email'), 'users', ['email'], unique=True)
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###

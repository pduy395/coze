"""add collum icon to table llm

Revision ID: f5e335e68b42
Revises: 43b6ec9c13f7
Create Date: 2024-08-12 11:55:52.460709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5e335e68b42'
down_revision: Union[str, None] = '43b6ec9c13f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('config_llm', sa.Column('icon', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('config_llm', 'icon')
    # ### end Alembic commands ###

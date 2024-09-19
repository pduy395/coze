"""add foreignkey in progress table

Revision ID: ed7efa0d08c5
Revises: 5802d308c93d
Create Date: 2024-08-23 16:20:06.288404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed7efa0d08c5'
down_revision: Union[str, None] = '5802d308c93d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'progress', 'knowledge', ['knowledge_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'progress', type_='foreignkey')
    # ### end Alembic commands ###

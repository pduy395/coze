"""fix knowledge tables

Revision ID: 8c95ab593e47
Revises: 7b20b5942785
Create Date: 2024-07-22 12:33:06.395591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c95ab593e47'
down_revision: Union[str, None] = '7b20b5942785'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('embed_type', sa.Column('embed_model', sa.String(), nullable=True))
    op.drop_constraint('knowledge_user_id_fkey', 'knowledge', type_='foreignkey')
    op.drop_column('knowledge', 'embed_model')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('knowledge', sa.Column('embed_model', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key('knowledge_user_id_fkey', 'knowledge', 'users', ['user_id'], ['id'], referent_schema='auth')
    op.drop_column('embed_type', 'embed_model')
    # ### end Alembic commands ###

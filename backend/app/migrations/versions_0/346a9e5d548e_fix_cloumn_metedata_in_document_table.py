"""fix cloumn metedata in document table

Revision ID: 346a9e5d548e
Revises: e0e40cc66ec4
Create Date: 2024-07-22 15:31:52.383897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '346a9e5d548e'
down_revision: Union[str, None] = 'e0e40cc66ec4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('document', 'meta_data',
               existing_type=sa.VARCHAR(),
               type_=sa.JSON(),
               postgresql_using='meta_data::json',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('document', 'meta_data',
               existing_type=sa.JSON(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    # ### end Alembic commands ###

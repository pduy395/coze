"""Added initial tables

Revision ID: 7b20b5942785
Revises: 
Create Date: 2024-07-22 11:29:18.924227

"""
from typing import Sequence, Union
import pgvector
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b20b5942785'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table('knowledge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('edit_time', sa.DateTime(), nullable=True),
    sa.Column('enable', sa.Boolean(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('format', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('embed_model', sa.String(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_id'), 'knowledge', ['id'], unique=False)
    op.create_table('embed_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('segment', sa.String(), nullable=True),
    sa.Column('max_length', sa.String(), nullable=True),
    sa.Column('rule_1', sa.Boolean(), nullable=True),
    sa.Column('rule_2', sa.Boolean(), nullable=True),
    sa.Column('knowledge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['knowledge_id'], ['knowledge.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_embed_type_id'), 'embed_type', ['id'], unique=False)
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('knowledge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['knowledge_id'], ['knowledge.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_id'), 'file', ['id'], unique=False)
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('vector', pgvector.sqlalchemy.vector.VECTOR(dim=1536), nullable=True),
    sa.Column('knowledge_id', sa.Integer(), nullable=True),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
    sa.ForeignKeyConstraint(['knowledge_id'], ['knowledge.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_id'), 'document', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP EXTENSION IF EXISTS vector;")
    op.drop_index(op.f('ix_document_id'), table_name='document')
    op.drop_table('document')
    op.drop_index(op.f('ix_file_id'), table_name='file')
    op.drop_table('file')
    op.drop_index(op.f('ix_embed_type_id'), table_name='embed_type')
    op.drop_table('embed_type')
    op.drop_index(op.f('ix_knowledge_id'), table_name='knowledge')
    op.drop_table('knowledge')
    # ### end Alembic commands ###

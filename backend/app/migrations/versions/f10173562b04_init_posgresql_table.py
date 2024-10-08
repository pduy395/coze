"""init posgresql table

Revision ID: f10173562b04
Revises: 
Create Date: 2024-08-20 09:22:54.578820

"""
from typing import Sequence, Union

from alembic import op
import pgvector
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f10173562b04'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table('chatbot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('favourite', sa.Boolean(), nullable=True),
    sa.Column('llm_name', sa.String(), nullable=True),
    sa.Column('updated_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chatbot_id'), 'chatbot', ['id'], unique=False)
    op.create_table('progress',
    sa.Column('knowledge_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('knowledge_id', 'file_id')
    )
    op.create_table('user_account',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('mail', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('personal_signature', sa.String(), nullable=True),
    sa.Column('alias', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_account_id'), 'user_account', ['id'], unique=False)
    op.create_table('config_llm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('top_p', sa.Float(), nullable=True),
    sa.Column('frequency_penalty', sa.Float(), nullable=True),
    sa.Column('presence_penalty', sa.Float(), nullable=True),
    sa.Column('dialog_round', sa.Integer(), nullable=True),
    sa.Column('max_length', sa.Integer(), nullable=True),
    sa.Column('output_format', sa.String(), nullable=True),
    sa.Column('config_type', sa.String(), nullable=True),
    sa.Column('llm_name', sa.String(), nullable=True),
    sa.Column('label', sa.String(), nullable=True),
    sa.Column('info', sa.String(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('chatbot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chatbot_id'], ['chatbot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_config_llm_id'), 'config_llm', ['id'], unique=False)
    op.create_table('knowledge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('edit_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('enable', sa.Boolean(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('format', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_id'), 'knowledge', ['id'], unique=False)
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('input_tokens', sa.Integer(), nullable=True),
    sa.Column('output_tokens', sa.Integer(), nullable=True),
    sa.Column('latency', sa.Integer(), nullable=True),
    sa.Column('chatbot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chatbot_id'], ['chatbot.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_id'), 'message', ['id'], unique=False)
    op.create_table('chatbot_knowledge',
    sa.Column('chatbot_id', sa.Integer(), nullable=False),
    sa.Column('knowledge_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chatbot_id'], ['chatbot.id'], ),
    sa.ForeignKeyConstraint(['knowledge_id'], ['knowledge.id'], ),
    sa.PrimaryKeyConstraint('chatbot_id', 'knowledge_id')
    )
    op.create_table('embed_type',
    sa.Column('knowledge_id', sa.Integer(), nullable=False),
    sa.Column('embed_model', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('segment', sa.String(), nullable=True),
    sa.Column('max_length', sa.String(), nullable=True),
    sa.Column('rule_1', sa.Boolean(), nullable=True),
    sa.Column('rule_2', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['knowledge_id'], ['knowledge.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('knowledge_id')
    )
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('knowledge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['knowledge_id'], ['knowledge.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_id'), 'file', ['id'], unique=False)
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('vector', pgvector.sqlalchemy.vector.VECTOR(), nullable=True),
    sa.Column('meta_data', sa.JSON(), nullable=True),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('knowledge_id', sa.Integer(), nullable=True),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['knowledge_id'], ['knowledge.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_id'), 'document', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_document_id'), table_name='document')
    op.drop_table('document')
    op.drop_index(op.f('ix_file_id'), table_name='file')
    op.drop_table('file')
    op.drop_table('embed_type')
    op.drop_table('chatbot_knowledge')
    op.drop_index(op.f('ix_message_id'), table_name='message')
    op.drop_table('message')
    op.drop_index(op.f('ix_knowledge_id'), table_name='knowledge')
    op.drop_table('knowledge')
    op.drop_index(op.f('ix_config_llm_id'), table_name='config_llm')
    op.drop_table('config_llm')
    op.drop_index(op.f('ix_user_account_id'), table_name='user_account')
    op.drop_table('user_account')
    op.drop_table('progress')
    op.drop_index(op.f('ix_chatbot_id'), table_name='chatbot')
    op.drop_table('chatbot')
    # ### end Alembic commands ###

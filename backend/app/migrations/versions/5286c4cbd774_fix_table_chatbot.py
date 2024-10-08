"""fix table chatbot

Revision ID: 5286c4cbd774
Revises: f10173562b04
Create Date: 2024-08-20 09:27:03.534909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5286c4cbd774'
down_revision: Union[str, None] = 'f10173562b04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'chatbot', 'user_account', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('chatbot_knowledge_knowledge_id_fkey', 'chatbot_knowledge', type_='foreignkey')
    op.drop_constraint('chatbot_knowledge_chatbot_id_fkey', 'chatbot_knowledge', type_='foreignkey')
    op.create_foreign_key(None, 'chatbot_knowledge', 'knowledge', ['knowledge_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'chatbot_knowledge', 'chatbot', ['chatbot_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('config_llm_chatbot_id_fkey', 'config_llm', type_='foreignkey')
    op.create_foreign_key(None, 'config_llm', 'chatbot', ['chatbot_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'config_llm', type_='foreignkey')
    op.create_foreign_key('config_llm_chatbot_id_fkey', 'config_llm', 'chatbot', ['chatbot_id'], ['id'])
    op.drop_constraint(None, 'chatbot_knowledge', type_='foreignkey')
    op.drop_constraint(None, 'chatbot_knowledge', type_='foreignkey')
    op.create_foreign_key('chatbot_knowledge_chatbot_id_fkey', 'chatbot_knowledge', 'chatbot', ['chatbot_id'], ['id'])
    op.create_foreign_key('chatbot_knowledge_knowledge_id_fkey', 'chatbot_knowledge', 'knowledge', ['knowledge_id'], ['id'])
    op.drop_constraint(None, 'chatbot', type_='foreignkey')
    # ### end Alembic commands ###

from database.db_service import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship 


class Knowledge(Base):
    __tablename__="knowledge"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    edit_time = Column(DateTime(timezone=True))
    enable = Column(Boolean)
    size = Column(Integer)
    icon = Column(String)
    format = Column(String)

    description = Column(String)
    user_id = Column(UUID(as_uuid=True),ForeignKey("user_account.id",ondelete='CASCADE'))

    user = relationship("User", back_populates="knowledges")
    chatbot_knowledges = relationship("Chatbot_Knowledge", back_populates="knowledge")
    files = relationship("File", back_populates="knowledge")
    documents = relationship("Document", back_populates="knowledge")
    embed_type = relationship("Embed_type", back_populates="knowledge",uselist=False)
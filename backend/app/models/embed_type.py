from database.db_service import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship 
import uuid


class Embed_type(Base):
    __tablename__="embed_type"
    knowledge_id = Column(Integer,ForeignKey("knowledge.id",ondelete='CASCADE'),primary_key=True)
    embed_model = Column(String)
    type = Column(String)
    segment = Column(String)
    max_length = Column(String)
    rule_1 = Column(Boolean)
    rule_2 = Column(Boolean)

    knowledge = relationship("Knowledge", back_populates="embed_type")
    
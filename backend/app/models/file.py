from database.db_service import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship 
import uuid

class File(Base):
    __tablename__="file"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    size = Column(Integer)
    knowledge_id = Column(Integer,ForeignKey("knowledge.id",ondelete='CASCADE'))

    knowledge = relationship("Knowledge", back_populates="files")
    documents = relationship("Document", back_populates="file")
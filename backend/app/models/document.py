from database.db_service import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, JSON, FLOAT
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship 
import uuid




class Document(Base):
    __tablename__="document"
    id = Column(UUID(as_uuid=True), primary_key=True,index=True,default=uuid.uuid4)
    content = Column(String)
    vector = Column(Vector)
    meta_data = Column(JSON)
    index = Column(Integer)
    knowledge_id = Column(Integer,ForeignKey("knowledge.id",ondelete='CASCADE'))
    file_id = Column(Integer,ForeignKey("file.id",ondelete='CASCADE'))

    knowledge = relationship("Knowledge", back_populates="documents")
    file = relationship("File", back_populates="documents")
    knowledge_id = Column(Integer,ForeignKey("knowledge.id",ondelete='CASCADE'))
    file_id = Column(Integer,ForeignKey("file.id",ondelete='CASCADE'))

    knowledge = relationship("Knowledge", back_populates="documents")
    file = relationship("File", back_populates="documents")

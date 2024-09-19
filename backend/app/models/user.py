from database.db_service import Base
from sqlalchemy import Column, Integer,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid




class User(Base):
    __tablename__="user_account"
    id = Column(UUID(as_uuid=True), primary_key=True,index=True,default=uuid.uuid4)
    username = Column(String)
    mail = Column(String)
    password = Column(String)
    avatar = Column(String)
    personal_signature = Column(String)
    alias = Column(String)

    knowledges = relationship("Knowledge", back_populates="user")
    
    

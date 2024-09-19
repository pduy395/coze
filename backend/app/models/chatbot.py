from database.db_service import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship 


class Chatbot(Base):
    __tablename__="chatbot"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    name = Column(String)
    user_id = Column(UUID(as_uuid=True))
    favourite = Column(Boolean)
    llm_name = Column(String)
    updated_time = Column(DateTime(timezone=True))
    description = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_account.id", ondelete="CASCADE"))

    chatbot_knowledges = relationship("Chatbot_Knowledge", back_populates="chatbot")
    llms = relationship("LLM", back_populates="chatbot")


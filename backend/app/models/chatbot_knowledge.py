from database.db_service import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Chatbot_Knowledge(Base):
    __tablename__="chatbot_knowledge"
    chatbot_id = Column(Integer, ForeignKey("chatbot.id", ondelete="CASCADE"), primary_key=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge.id", ondelete="CASCADE"), primary_key=True)

    chatbot = relationship("Chatbot", back_populates="chatbot_knowledges")
    knowledge = relationship("Knowledge", back_populates="chatbot_knowledges")
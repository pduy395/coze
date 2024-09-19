from database.db_service import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

class LLM(Base):
    __tablename__="config_llm"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    top_p = Column(Float)
    frequency_penalty = Column(Float)
    presence_penalty = Column(Float)
    dialog_round = Column(Integer)
    max_length = Column(Integer)
    output_format = Column(String)
    config_type = Column(String)
    llm_name = Column(String)
    label = Column(String)
    info = Column(String)
    icon = Column(String)   
    chatbot_id = Column(Integer, ForeignKey("chatbot.id", ondelete="CASCADE"))

    chatbot = relationship("Chatbot", back_populates="llms")
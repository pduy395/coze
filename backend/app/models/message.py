from database.db_service import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime


class Message(Base):
    __tablename__="message"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime(timezone=True))
    question = Column(String)
    answer = Column(String)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    latency = Column(Integer)
    chatbot_id = Column(Integer, ForeignKey("chatbot.id", ondelete="CASCADE"))
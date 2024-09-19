from pydantic import BaseModel
from datetime import datetime, timezone

class MessageResponse(BaseModel):
    answer: str
    input_tokens: int
    output_tokens: int

class MessageBase(MessageResponse):
    time: datetime = datetime.now(timezone.utc).astimezone()
    question: str
    latency: int = 0
    

class Message(MessageBase):
    chat_id: int

class Question(BaseModel):
    question: str
from pydantic import BaseModel
from datetime import datetime

class ChatbotBase(BaseModel):
    prompt: str = ''
    name: str
    description: str
    llm_name: str = 'Gemini 1.5 Flash'
    updated_time: datetime = datetime.now()
    favourite: bool = False

class Chatbot(ChatbotBase):
    user_id: str

class PromptBase(BaseModel):
    prompt: str
    updated_time: datetime = datetime.now()

class LLMLabel (BaseModel):
    llm_name: str
    updated_time: datetime = datetime.now()

class UpdatedTime(BaseModel):
    updated_time: datetime = datetime.now()

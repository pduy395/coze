from pydantic import BaseModel

class ChatbotKnowledge(BaseModel):
    chatbot_id: int
    knowledge_id: int

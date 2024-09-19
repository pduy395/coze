from pydantic import BaseModel

class LLMBase(BaseModel):
    temperature: float = 0.5
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0
    dialog_round: int = 3
    max_length: int = 1024
    output_format: str = 'text'
    config_type: str = 'custom'

class LLM(LLMBase):
    llm_name: str = 'gemini-1.5-pro'
    label: str = 'Gemini 1.5 Pro'
    info: str = ''
    chatbot_id: int
    icon: str

class LLMType(BaseModel):
    config_type: str
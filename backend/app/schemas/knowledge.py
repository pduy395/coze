from pydantic import BaseModel, UUID4
from datetime import datetime


class KnowledgeCreate(BaseModel):
    icon: str = "https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/text_icon.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvdGV4dF9pY29uLnBuZyIsImlhdCI6MTcyMTU4NDgyOCwiZXhwIjoxNzUzMTIwODI4fQ.N_Xd8Td6an-tkh_arQs5pyZ1FzvKSiyvgCPcYPwk8io&t=2024-07-21T18%3A00%3A31.505Z"
    description: str
    format: str = "text"
    name: str


    

class Knowledge_res(KnowledgeCreate):
    enable: bool = True
    edit_time: datetime 
    id:int
    class Config():
        from_attributes = True

class File(BaseModel):
    knowledge_id: int
    id: int
    name: str

class Document(BaseModel):
    content: str
    vector: list[float]
    file_id: int
    knowledge_id: int
    metadata: dict


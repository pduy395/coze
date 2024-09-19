from pydantic import BaseModel, UUID4
from datetime import datetime

class File_rename(BaseModel):
    name: str

class UploadURL(BaseModel):
    url: str

class url_data(BaseModel):
    name:str
    content:str

class File(File_rename):
    id:int
    
    class Config():
        from_attributes = True


class Embed_type(BaseModel):
    embed_model:str = "simCSE"
    segment: str = "\n"
    max_length: int = 1000
    rule_1: bool = 1
    rule_2:bool = 1

class Document(BaseModel):
    content:str
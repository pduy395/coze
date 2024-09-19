from pydantic import BaseModel, Field
import string
import random
from typing import Optional

def generate_random_alias(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


from pydantic import BaseModel

class UserUpdate(BaseModel):
    username: str
    personal_signature:str = ""
    alias :str = "alias"

class UserShow(UserUpdate):
    avatar: str = "https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/avatar.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvYXZhdGFyLnBuZyIsImlhdCI6MTcyMzU0MTM4NywiZXhwIjoxNzU1MDc3Mzg3fQ.x153QGUkzVo2f9SMxvAz_icx6SGH6ZtJDKq9c6z4bQ8&t=2024-08-13T09%3A29%3A49.019Z"
    mail: str
    class Config():
        from_attributes = True

class User(UserShow):
    password: str


class UserLogin(BaseModel):
    mail: str
    password: str

class ChangePassword(BaseModel):
    old_password:str
    new_pass:str

from fastapi import FastAPI, APIRouter
import uvicorn
from pydantic import BaseModel
import torch
from sentence_transformers import SentenceTransformer
from fastapi import HTTPException, status
import random


router = APIRouter(tags=["Embedding"], prefix='/embedding')

class Text(BaseModel):
    text: str


list_model = []
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

for i in range(3):
    model = SentenceTransformer('pkshatech/GLuCoSE-base-ja')
    model = model.to(device)
    list_model.append(model)


@router.post("")
async def embedding(request: Text):
    try:
        model = random.choice(list_model)
        embedding = model.encode(request.text).tolist()
        return embedding
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.args,
            )

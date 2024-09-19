from fastapi import WebSocket, WebSocketDisconnect, Query, BackgroundTasks, Security, Depends
from fastapi import APIRouter, Depends, HTTPException, status, WebSocketException
from supabase import Client
from typing import Annotated, List, Optional
from database.db_service import get_supabase
from utils.JWTtoken import get_id
from router.message import generate_message
from utils.optimize_prompt import optimize_prompt
from schemas.message import Question
from service.chatbot import check_onwership
from sentence_transformers import SentenceTransformer
from database.db_service import get_postgresql
import gc

router = APIRouter(tags=["Socket"],prefix="/ws")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/generate/{chatbot_id}")
async def generate(
    websocket: WebSocket,
    chatbot_id,
    token: Optional[str] = Query(None),
    session: Client = Depends(get_postgresql),
):
    await manager.connect(websocket)
    try:
        user_id = get_id(token)
        await check_onwership(user_id, chatbot_id, session)
        await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        return WebSocketException(
            code=status.WS_1000_NORMAL_CLOSURE,
            reason="Connection closed",
        )
    except Exception as e:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION,reason=str(e)[5:])
    try:
        model = SentenceTransformer('pkshatech/GLuCoSE-base-ja', device='cpu')
        # model = None
        while True:
            data = await websocket.receive_text()
            await generate_message(user_id, chatbot_id, Question(question=data), websocket, session, model)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        return WebSocketException(
            code=status.WS_1000_NORMAL_CLOSURE,
            reason="Connection closed",
        )
    finally:
        del model
        gc.collect()


@router.websocket("/optimize-prompt")
async def get_optimize_prompt(
    websocket: WebSocket,
    token: str,
):
    await manager.connect(websocket)

    try:
        user_id = get_id(token)
    except Exception as e:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION,reason=str(e)[5:])
    
    
    try:
        while True:
            data = await websocket.receive_text()
            await optimize_prompt (data, websocket)
            await websocket.send_text("EOS-8000")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        return WebSocketException(
            code=status.WS_1000_NORMAL_CLOSURE,
            reason="Connection closed",
        )

from fastapi import APIRouter, Depends, Security, HTTPException, status
from typing import Annotated, List
from schemas.message import Question, MessageBase
from utils.JWTtoken import get_id
from utils.generate import generate_answer
from utils.exceptions import BAD_REQUEST, FORBIDDEN, NOT_FOUND
from service.config_llm import get_config_llm
from fastapi.encoders import jsonable_encoder
import time
import service.chatbot
from repository.message import MessageDBPostgreSql
from repository.chatbot import ChatbotDBPostgreSql
from repository.config_llm import ConfigLLMDBPostgreSql
from repository.chatbot_knowledge import ChatbotKnowledgeDBPostgreSql
from service.retrieval import get_similarity_document
from database.db_service import get_postgresql
from sqlalchemy.orm import Session

message_db = MessageDBPostgreSql()
chatbot_db = ChatbotDBPostgreSql()
config_llm_db = ConfigLLMDBPostgreSql()
chatbot_knowledge_db = ChatbotKnowledgeDBPostgreSql()



router = APIRouter(tags=["Message"],prefix="/message")

@router.get("/chatbot/{chatbot_id}") 
async def get_messages(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_onwership(user_id, chatbot_id, session)
    try:
        messages = await message_db.get_message_by_chatbot_id(chatbot_id, offset, limit+offset, session)
        return messages
    except Exception as e:
        raise NOT_FOUND

@router.post("/chatbot/{chatbot_id}")
async def create_message(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    message: MessageBase,
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_onwership(user_id, chatbot_id, session)
    try:
        message_data = jsonable_encoder(message)
        message_data['chatbot_id'] = chatbot_id
        created_message = await message_db.create_message(message_data, session)
        return {"detail": "Message created successfully",
                "id": created_message['id']}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )

@router.delete("/{message_id}")    
async def delete_message(
    user_id: Annotated[str, Security(get_id)],
    message_id: int,
    session: Session = Depends(get_postgresql)
):
    try:
        message = await message_db.get_message_by_id(message_id, session)
        await service.chatbot.check_onwership(user_id, message['chatbot_id'], session)
        await message_db.delete_message(message_id, session)
        return {"detail": "Message deleted successfully"}
    except Exception as e:
        raise NOT_FOUND

@router.delete("/history/{chatbot_id}")
async def delete_all_messages(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_onwership(user_id, chatbot_id, session)
    try:
        await message_db.delete_all_messages(chatbot_id, session)
        return {"detail": "History deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )
    

async def generate_message(
    user_id: str,
    chatbot_id: int,
    question: Question,
    websocket,
    session: Depends,
    model
):
    try:
        start = time.time()
        chatbot = await chatbot_db.get_chatbot_by_id(user_id, chatbot_id, session)
        knowledges = await chatbot_knowledge_db.get_chatbot_knowledge_by_chatbot_id(chatbot_id, session)
        knowledge_ids = [knowledge['knowledge_id'] for knowledge in knowledges]
        if (len(knowledge_ids) != 0):
            retrievals = await get_similarity_document(knowledge_ids, question.question, session, model)
            # print(retrievals)
            context = "\n".join([retrieval['content'] for retrieval in retrievals])
        else: 
            context = "----"
        config_llm = await get_config_llm(chatbot_id, chatbot['llm_name'], session)
        instruction = chatbot['prompt']
        chats = await message_db.get_message_by_chatbot_id(chatbot_id, 0, config_llm['dialog_round'], session)
        response = await generate_answer(
            instruction=instruction,
            chats=chats,
            context=context,
            question=question.question,
            config_llm=config_llm,
            websocket=websocket
        )
        end = time.time()
        response.latency = round((end - start)*1000)
        # print (jsonable_encoder(response))
        await websocket.send_json(jsonable_encoder(response))

    
    except Exception as e:
        raise NOT_FOUND

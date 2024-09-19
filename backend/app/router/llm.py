from fastapi import APIRouter, Depends, Security, HTTPException, status
from utils.JWTtoken import get_id
from utils.exceptions import BAD_REQUEST, FORBIDDEN, NOT_FOUND
from fastapi.encoders import jsonable_encoder
import service.chatbot
from repository.config_llm import ConfigLLMDBPostgreSql
from repository.chatbot import ChatbotDBPostgreSql
from database.db_service import get_postgresql
from sqlalchemy.orm import Session
from schemas.config_llm import LLMBase

config_llm_db = ConfigLLMDBPostgreSql()
chatbot_db = ChatbotDBPostgreSql()


router = APIRouter(tags=["LLM"],prefix="/llm")

@router.get('/chatbot/{chatbot_id}')
async def get_config_llm(
    chatbot_id: int,
    user_id: int = Security(get_id),
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_onwership(user_id, chatbot_id, session)
    try:
        config_llms = await config_llm_db.get_config_llm_by_chatbot_id(chatbot_id, session)
        return config_llms
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )

@router.get('/{config_llm_id}')
async def get_config_llm_by_id(
    config_llm_id: int,
    user_id: int = Security(get_id),
    session: Session = Depends(get_postgresql)
):
    try:
        config_llm, id = await config_llm_db.get_config_llm_by_id(config_llm_id, session)
        if (str(id) != user_id):
            raise NOT_FOUND
        if config_llm['label'][:6] == 'Gemini':
            config_llm.pop('frequency_penalty')
            config_llm.pop('presence_penalty')
        config_llm.pop('chatbot')
        return config_llm
    except:
        raise NOT_FOUND    

@router.patch('/{config_llm_id}')
async def update_config_llm(
    config_llm_id: int,
    config_llm: LLMBase,
    user_id: int = Security(get_id),
    session: Session = Depends(get_postgresql)
):
    try:
        config_llm_data, id = await config_llm_db.get_config_llm_by_id(config_llm_id, session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )
    if (str(id) != user_id):
        raise NOT_FOUND
    try:
        config_llm = jsonable_encoder(config_llm)
        if config_llm['config_type'] != 'custom' :
            config_llm['temperature'] = config_llm_data['temperature']
            config_llm['top_p'] = config_llm_data['top_p']
            config_llm['frequency_penalty'] = config_llm_data['frequency_penalty']
            config_llm['presence_penalty'] = config_llm_data['presence_penalty']

        updated_config_llm = await config_llm_db.update_config_llm_by_id(config_llm_id, config_llm, session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )
    if len(updated_config_llm) == 0:
        raise NOT_FOUND
    else:
        try: 
            chatbot_id = config_llm_data['chatbot_id']
            chatbot_updated = await chatbot_db.update_time_by_id(chatbot_id, session)
            return {"detail": "successfully updated llm",
                    "updated_time" : chatbot_updated[0]['updated_time']}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.args[0],
            )
        

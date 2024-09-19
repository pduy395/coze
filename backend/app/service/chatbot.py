from fastapi import Depends, HTTPException, status
from utils.exceptions import NOT_FOUND
from repository.chatbot import ChatbotDBSupabase, ChatbotDBPostgreSql

chatbot_db = ChatbotDBPostgreSql()

async def check_chatbot_exists(
    chatbot_name: str,
    user_id: int,
    chatbot_id: int,
    session: Depends
):
    try :
        chatbot = await chatbot_db.get_chatbot_by_name(user_id, chatbot_name, session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    if len (chatbot) > 0 :
        if chatbot_id != chatbot[0]['id']:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chatbot name already exists",
        ) 

async def check_onwership(
    user_id: int,
    chatbot_id: int,
    session: Depends
):
    try:
        await chatbot_db.get_chatbot_by_id(user_id, chatbot_id, session)
    except Exception as e:
        raise NOT_FOUND
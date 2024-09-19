from fastapi import APIRouter, Depends, Security, HTTPException, status
from supabase import Client
from typing import Annotated, List
from database.db_service import get_supabase
from schemas.chatbot import ChatbotBase, PromptBase, LLMLabel, Chatbot
from schemas.config_llm import LLM
from schemas.chatbot_knowledge import ChatbotKnowledge
from utils.JWTtoken import get_id
from utils.exceptions import BAD_REQUEST, FORBIDDEN, NOT_FOUND
from utils.optimize_prompt import optimize_prompt
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone
import service.chatbot
import random
from sqlalchemy.orm import Session
from repository.chatbot import ChatbotDBSupabase, ChatbotDBPostgreSql
from repository.config_llm import ConfigLLMDBSupabase, ConfigLLMDBPostgreSql
from repository.chatbot_knowledge import ChatbotKnowledgeDBSupabase, ChatbotKnowledgeDBPostgreSql
from database.db_service import get_postgresql

chatbot_db = ChatbotDBPostgreSql()
config_llm_db = ConfigLLMDBPostgreSql()
chatbot_knowledge_db = ChatbotKnowledgeDBPostgreSql()
chatbot_db = ChatbotDBPostgreSql()
config_llm_db = ConfigLLMDBPostgreSql()
chatbot_knowledge_db = ChatbotKnowledgeDBPostgreSql()

models = [
    {
        'name': 'gpt-3.5-turbo-0125',
        'label': 'Gpt-3.5 Turbo',
        'info': 'A fast, inexpensive model for simple tasks\nContext window 16k tokens',
        'icon': 'https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/chatgpt-icon.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvY2hhdGdwdC1pY29uLmpwZyIsImlhdCI6MTcyMzQ1NTczOCwiZXhwIjoyMzU0MTc1NzM4fQ.2FaCyo_nZwtZxEiJizdqwwmBU7RYmqr0aFh0bau5mEI&t=2024-08-12T09%3A42%3A18.412Z'
    },
    {
        'name': 'gpt-4o-mini',
        'label': 'Gpt-4o Mini',
        'info': 'Our affordable and intelligent small model for fast, lightweight tasks\nContext window 128k tokens',
        'icon': 'https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/chat-gpt.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvY2hhdC1ncHQucG5nIiwiaWF0IjoxNzIzNDQxMDE0LCJleHAiOjQ4NzcwNDEwMTR9.s-7Vh1D1x2vBO3ppWZ6K5u5JNXx9ACHQByWQwYi5E1E&t=2024-08-12T05%3A36%3A54.344Z'
    },
    {
        'name': 'gpt-4o',
        'label': 'Gpt-4o',
        'info': 'Our high-intelligence flagship model for complex, multi-step tasks\nContext window 128k tokens',
        'icon': 'https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/chat-gpt.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvY2hhdC1ncHQucG5nIiwiaWF0IjoxNzIzNDQxMDE0LCJleHAiOjQ4NzcwNDEwMTR9.s-7Vh1D1x2vBO3ppWZ6K5u5JNXx9ACHQByWQwYi5E1E&t=2024-08-12T05%3A36%3A54.344Z'
    },
    {
        'name': 'gemini-1.5-flash',
        'label': 'Gemini 1.5 Flash',
        'info': 'Gemini 1.5 Flash is a fast and versatile multimodal model for scaling across diverse tasks.\nInput token limit 1M',
        'icon': 'https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/google-gemini-icon.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvZ29vZ2xlLWdlbWluaS1pY29uLnBuZyIsImlhdCI6MTcyMzQ0Mzc0OCwiZXhwIjoyMzU0MTYzNzQ4fQ.V4iGROWxbUA-PxWAN-bzMNEhY6Z-qSTYKUHmmfUz8WU&t=2024-08-12T06%3A22%3A28.698Z'
    },
    {
        'name': 'gemini-1.5-pro',
        'label': 'Gemini 1.5 Pro',
        'info': 'Gemini 1.5 Pro is a mid-size multimodal model that is optimized for a wide-range of reasoning tasks. 1.5 Pro can process large amounts of data at once, including 2 hours of video, 19 hours of audio, codebases with 60,000 lines of code, or 2,000 pages of text.\nInput token limit 2M',
        'icon': 'https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/google-gemini-icon.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvZ29vZ2xlLWdlbWluaS1pY29uLnBuZyIsImlhdCI6MTcyMzQ0Mzc0OCwiZXhwIjoyMzU0MTYzNzQ4fQ.V4iGROWxbUA-PxWAN-bzMNEhY6Z-qSTYKUHmmfUz8WU&t=2024-08-12T06%3A22%3A28.698Z'
    },
    {
        'name': 'lmstudio-ai/gemma-2b-it-GGUF/gemma-2b-it-q8_0.gguf',
        'label': 'Gemma',
        'info': 'Gemma is a family of lightweight, state-of-the-art open models from Google, built from the same research and technology used to create the Gemini models.\nModels are trained on a context length of 8192 tokens, this model card corresponds to the 2B base version of the Gemma model.',
        'icon': 'https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/google-gemini-icon.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvZ29vZ2xlLWdlbWluaS1pY29uLnBuZyIsImlhdCI6MTcyMzQ0Mzc0OCwiZXhwIjoyMzU0MTYzNzQ4fQ.V4iGROWxbUA-PxWAN-bzMNEhY6Z-qSTYKUHmmfUz8WU&t=2024-08-12T06%3A22%3A28.698Z'
    },
    {
        'name': 'lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf',
        'label': 'Llama 3.1',
        'info': 'Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B sizes.\nThe Llama 3 instruction tuned models are optimized for dialogue use cases and outperform many of the available open source chat models on common industry benchmarks.',
        'icon': 'https://oosfnrvamovijfkscfbf.supabase.co/storage/v1/object/sign/avatar/meta.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJhdmF0YXIvbWV0YS5wbmciLCJpYXQiOjE3MjM0NDI5MDAsImV4cCI6MjM1NDE2MjkwMH0.mqYBBYiFXK_Oe0avGSTzHwdNb3YydgygIhPmVPoyczA&t=2024-08-12T06%3A08%3A20.615Z'
    },
]

router = APIRouter(tags=["Chatbot"],prefix="/chatbot")

@router.post("")
async def create_chatbot(
    chatbot: ChatbotBase,
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_chatbot_exists(chatbot.name, user_id, -1, session)
    try:
        chatbot_data = jsonable_encoder(chatbot)
        chatbot_data['updated_time'] = datetime.now(timezone.utc).astimezone().isoformat()
        chatbot_data["user_id"] = user_id
        chatbot_created = await chatbot_db.create_chatbot(chatbot_data, session)
        config_llm_datas = [jsonable_encoder( 
                LLM(        
                    llm_name=model['name'], 
                    label=model['label'], 
                    info=model['info'], 
                    icon=model['icon'],
                    chatbot_id=chatbot_created['id']
                    ))
            for model in models]
        
        await config_llm_db.create_multi_config_llm(config_llm_datas, session)
       
        return {"detail": "Chatbot created successfully",
                "id": chatbot_created['id'],
                "updated_time" : chatbot_created['updated_time']}
                
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.args),
        )

@router.get("/all")
async def get_all_chatbots(
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        return await chatbot_db.get_chatbot_by_user_id(user_id, session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )

@router.get("/{chatbot_id}")
async def get_chatbot_by_id(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    session: Session = Depends(get_postgresql)
): 
    try:
        return await chatbot_db.get_chatbot_by_id(user_id, chatbot_id, session)
    except Exception as e:
        raise NOT_FOUND
    

@router.post("/{chatbot_id}/duplicate")
async def duplicate_chatbot(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    session: Session = Depends(get_postgresql)
):
    try:
        chatbot = await chatbot_db.get_chatbot_by_id(user_id, chatbot_id, session)
        chatbot.pop("id")
        chatbot["name"] = chatbot["name"] + ''.join([str(random.randint(0, 9)) for _ in range(3)])
        chatbot["favourite"] = False 
        chatbot["updated_time"] = datetime.now(timezone.utc).astimezone().isoformat()
        chatbot["user_id"] = user_id
        

        chatbot_data = jsonable_encoder(Chatbot(**chatbot))
        copy_chatbot = await chatbot_db.create_chatbot(chatbot_data, session)

        configs = await config_llm_db.get_config_llm_by_chatbot_id(chatbot_id, session)
        for config in configs:
            config.pop("id")
            config["chatbot_id"] = copy_chatbot["id"]
        config_datas = [jsonable_encoder(LLM(**config)) for config in configs]
        await config_llm_db.create_multi_config_llm(config_datas, session)

        knowledges = await chatbot_knowledge_db.get_chatbot_knowledge_by_chatbot_id(chatbot_id, session)

        if len(knowledges) != 0:
            for knowledge in knowledges:
                knowledge["chatbot_id"] = copy_chatbot["id"]
        
        chatbot_knowledges_data = [jsonable_encoder(ChatbotKnowledge(**knowledge)) for knowledge in knowledges]
        await chatbot_knowledge_db.create_multi_chatbot_knowledge(chatbot_knowledges_data, session)

        return {"detail": "successfully duplicated chatbot",
                "copy_chatbot": copy_chatbot}
               
        
    except Exception as e:
        raise NOT_FOUND
    

@router.patch("/{chatbot_id}")
async def update_chatbot(
    chatbot_id: int,
    chatbot: ChatbotBase,
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_chatbot_exists(chatbot.name, user_id, chatbot_id, session)
    try:
        chatbot_data = jsonable_encoder(chatbot)
        chatbot_data['updated_time'] = datetime.now(timezone.utc).astimezone().isoformat()
        chatbot_updated = await chatbot_db.update_chatbot_by_id(user_id, chatbot_id, chatbot_data, session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )
    if len(chatbot_updated) == 0:
            raise NOT_FOUND
    return {"detail": "Chatbot updated successfully",
            "updated_time" : chatbot_data['updated_time']}
           



@router.patch("/{chatbot_id}/prompt")
async def update_chatbot(
    chatbot_id: int,
    prompt: PromptBase,
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        update_data = jsonable_encoder(prompt)
        update_data['updated_time'] = datetime.now(timezone.utc).astimezone().isoformat()
        chatbot_updated = await chatbot_db.update_chatbot_by_id(user_id, chatbot_id, update_data, session)
       
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )
    if len(chatbot_updated) == 0:
        raise NOT_FOUND
    return {"detail": "Chatbot updated successfully",
            "updated_time" : update_data['updated_time']}
            


@router.patch("/{chatbot_id}/llm_label")
async def update_chatbot_llm_label(
    chatbot_id: int,
    llm_label: LLMLabel,
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        update_data = jsonable_encoder(llm_label)
        update_data['updated_time'] = datetime.now(timezone.utc).astimezone().isoformat()
        chatbot_updated = await chatbot_db.update_chatbot_by_id(user_id, chatbot_id, update_data, session)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )

    if len(chatbot_updated) == 0:
            raise NOT_FOUND
    return {"detail": "Chatbot updated successfully",
            "updated_time" : update_data['updated_time']}
            
    

@router.delete("/{chatbot_id}")
async def delete_chatbot(
    chatbot_id: int,
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        chatbot_deleted = await chatbot_db.delete_chatbot_by_id(user_id, chatbot_id, session)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )

    if len(chatbot_deleted) == 0:
        raise NOT_FOUND
    return {"detail": "Chatbot deleted successfully"}
    

@router.post("/{chatbot_id}/knowledge/{knowledge_id}")
async def add_knowledge(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    knowledge_id: int,
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_onwership(user_id, chatbot_id, session)
    try:
        chatbot_knowledge_data = jsonable_encoder(
            ChatbotKnowledge(
                chatbot_id=chatbot_id, 
                knowledge_id=knowledge_id
            ))
        await chatbot_knowledge_db.create_chatbot_knowledge(chatbot_knowledge_data, session)
        chatbot_updated = await chatbot_db.update_time_by_id(chatbot_id, session)

        return {"detail": "successfully added knowledge",
            "updated_time" : chatbot_updated[0]['updated_time']}
   
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='knowledge is already added or not existed',
        )
    
@router.delete("/{chatbot_id}/knowledge/{knowledge_id}")
async def delete_knowledge(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    knowledge_id: int,
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_onwership(user_id, chatbot_id, session)

    try:       
        chatbot_knowledge_deleted = await chatbot_knowledge_db.delete_chatbot_knowledge(chatbot_id, knowledge_id, session)
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )
    
    if len(chatbot_knowledge_deleted) == 0 :
            raise NOT_FOUND
    else:
        try:
            chatbot_updated = await chatbot_db.update_time_by_id(chatbot_id, session)
            return {"detail": "successfully removed knowledge",
                    "updated_time" : chatbot_updated[0]['updated_time']}
        except Exception as e: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.args[0],
            )
        
@router.get("/{chatbot_id}/knowledge")
async def get_knowledge(
    user_id: Annotated[str, Security(get_id)],
    chatbot_id: int,
    session: Session = Depends(get_postgresql)
):
    await service.chatbot.check_onwership(user_id, chatbot_id, session)
    try:
        return await chatbot_knowledge_db.get_detail_chatbot_knowledge_by_chatbot_id(chatbot_id, session)
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0],
        )

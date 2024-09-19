from typing import List
from database.db_service import get_supabase
from models.config_llm import LLM
from models.chatbot import Chatbot
from fastapi import Depends


supabase_server = get_supabase()
# session = SessionLocal()

class ConfigLLMDB:
    def __init__(self):
        pass

    async def create_config_llm(
        self,
        config_llm: dict,
    ):
        pass

    async def create_multi_config_llm(
        self,
        config_llms: List[dict],
    ):
        pass
    async def get_config_llm_by_chatbot_id(
        self,
        chatbot_id: int,
    ):
        pass

    async def get_config_llm_by_chatbot_id_and_label(
        self,
        chatbot_id: int,
        llm_label: str,
    ):
        pass
    
    async def update_config_llm_by_id(
        self,
        config_llm_id: int,
        config_llm: dict,
    ):
        pass

    async def get_config_llm_by_id(
        self,
        config_llm_id: int,
        user_id: int,
    ):
        pass

class ConfigLLMDBSupabase(ConfigLLMDB):
    def __init__(self, supabase=supabase_server):
        self.supabase = supabase    

    async def create_config_llm(
        self,
        config_llm: dict,
    ):
        config_created = self.supabase.table("config_llm").insert(config_llm).execute().data
        return config_created

    async def create_multi_config_llm(
        self,
        config_llms: List[dict],
    ):
        config_created = self.supabase.table("config_llm").insert(config_llms).execute().data
        return config_created

    async def get_config_llm_by_chatbot_id(
        self,
        chatbot_id: int,
    ):
        config_llms = self.supabase.table("config_llm").select("*").eq("chatbot_id", chatbot_id).order("id", desc=False).execute().data
        return config_llms

    async def get_config_llm_by_chatbot_id_and_label(
        self,
        chatbot_id: int,
        llm_label: str,
    ):
        config_llm = self.supabase.table("config_llm").select("*").eq("chatbot_id", chatbot_id).eq("label", llm_label).execute().data
        return config_llm[0]
    
    async def update_config_llm_by_id(
        self,
        config_llm_id: int,
        config_llm: dict,
    ):
        updated_config_llm = self.supabase.table("config_llm").update(config_llm).eq("id", config_llm_id).execute().data
        return updated_config_llm

    async def get_config_llm_by_id(
        self,
        config_llm_id: int,
    ):
        config_llm = self.supabase.table("config_llm").select("*").eq("id", config_llm_id).execute().data[0]   
        config_llm = self.supabase.table("config_llm").select("*").eq("id", config_llm_id).execute().data[0]   
        return config_llm
    

class ConfigLLMDBPostgreSql(ConfigLLMDB):
    def __init__(self):
        pass

    async def create_config_llm(
        self,
        config_llm: dict,
        session: Depends
    ):
        config_created = LLM(**config_llm)
        session.add(config_created)
        session.commit()
        return config_created

    async def create_multi_config_llm(
        self,
        config_llms: List[dict],
        session: Depends
    ):
        config_createds = [LLM(**config_llm) for config_llm in config_llms]
        print(config_createds)
        session.add_all(config_createds)
        session.commit()
        return 'success'

    async def get_config_llm_by_chatbot_id(
        self,
        chatbot_id: int,
        session: Depends
    ):
        config_llms = session.query(LLM).filter(LLM.chatbot_id == chatbot_id).order_by(LLM.id).all()
        return [config_llm.__dict__ for config_llm in config_llms]

    async def get_config_llm_by_chatbot_id_and_label(
        self,
        chatbot_id: int,
        llm_label: str,
        session: Depends
    ):
        config_llm = session.query(LLM).filter(LLM.chatbot_id == chatbot_id).filter(LLM.label == llm_label).first()
        return config_llm.__dict__
    
    async def update_config_llm_by_id(
        self,
        config_llm_id: int,
        config_llm: dict,
        session: Depends
    ):
        updated_config_llm = session.query(LLM).filter(LLM.id == config_llm_id)
        if updated_config_llm:
            updated_config_llm.update(config_llm)
            session.commit()
            return updated_config_llm.all()
        else:
            return []

    async def get_config_llm_by_id(
        self,
        config_llm_id: int,
        session: Depends
    ):
        config_llm = session.query(LLM).filter(LLM.id == config_llm_id).first()
    
        return config_llm.__dict__, config_llm.chatbot.user_id
    

# async def create_config_llm(
#     config_llm: dict,
#     supabase: Depends
# ):
#     config_created = supabase.table("config_llm").insert(config_llm).execute().data
#     return config_created

# async def create_multi_config_llm(
#     config_llms: List[dict],
#     supabase: Depends
# ):
#     for config_llm in config_llms:
#         config_created = supabase.table("config_llm").insert(config_llm).execute().data
#     return config_created

# async def get_config_llm_by_chatbot_id(
#     chatbot_id: int,
#     supabase: Depends
# ):
#     config_llms = supabase.table("config_llm").select("*").eq("chatbot_id", chatbot_id).order("id", desc=False).execute().data
#     return config_llms

# async def get_config_llm_by_chatbot_id_and_label(
#     chatbot_id: int,
#     llm_label: str,
#     supabase: Depends
# ):
#     config_llm = supabase.table("config_llm").select("*").eq("chatbot_id", chatbot_id).eq("label", llm_label).execute().data
#     return config_llm[0]
   
# async def update_config_llm_by_id(
#     config_llm_id: int,
#     config_llm: dict,
#     supabase: Depends
# ):
#     updated_config_llm = supabase.table("config_llm").update(config_llm).eq("id", config_llm_id).execute().data
#     return updated_config_llm


# async def get_config_llm_by_id(
#     config_llm_id: int,
#     user_id: int,
#     supabase: Depends
# ):
#     config_llm = supabase.table("config_llm").select("*, chatbot(user_id)").eq("chatbot.user_id", user_id).eq("id", config_llm_id).execute().data[0]   
#     return config_llm

from fastapi import Depends
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models.chatbot import Chatbot


class ChatbotDB:
    def __init__(self):
        pass
    
    async def create_chatbot(
        self,
        chatbot: dict
    ):
        pass
    
    async def get_chatbot_by_user_id(
        self,
        user_id: int
    ):
        pass

    async def get_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int,
    ):
        pass
    
    async def get_chatbot_by_name(
        self,
        user_id: int,
        chatbot_name: str,
    ):
        pass
    async def update_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int,
        chatbot: dict
    ):
        pass

    async def update_time_by_id(
        self,
        chatbot_id: int
    ):
        pass

    async def delete_chatbot_by_id():
        pass


class ChatbotDBSupabase(ChatbotDB):
    def __init__(sel):
        pass

    async def create_chatbot(
        self,
        chatbot: dict
    ):
        chatbot_created = self.supabase.table("chatbot").insert(chatbot).execute().data
        return chatbot_created[0]
        return chatbot_created[0]
    
    async def get_chatbot_by_user_id(
        self,
        user_id: int
    ):
        chatbots = self.supabase.table("chatbot").select("*").eq("user_id", user_id).order("updated_time", desc=True).execute().data
        return chatbots

    async def get_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int,
    ):
        chatbot = self.supabase.table("chatbot").select("*").eq("id", chatbot_id).eq("user_id", user_id).execute().data
        return chatbot[0]
    
    async def get_chatbot_by_name(
        self,
        user_id: int,
        chatbot_name: str,
    ):
        chatbot = self.supabase.table("chatbot").select("*").eq("name", chatbot_name).eq("user_id", user_id).execute().data
        return chatbot

    async def update_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int,
        chatbot: dict
    ):
        chatbot_updated = self.supabase.table("chatbot").update(chatbot).eq("id", chatbot_id).eq("user_id", user_id).execute().data
        return chatbot_updated

    async def update_time_by_id(
        self,
        chatbot_id: int
    ):
        chatbot_updated = self.supabase.table("chatbot").update(
                {"updated_time":datetime.now(timezone.utc).astimezone().isoformat()}
            ).eq("id", chatbot_id).execute().data
        return chatbot_updated

    async def delete_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int
    ):
        chatbot_deleted = self.supabase.table("chatbot").delete().eq("id", chatbot_id).eq("user_id", user_id).execute().data
        return chatbot_deleted


class ChatbotDBPostgreSql(ChatbotDB):
    def __init__(self):
        # session = session
        pass

    async def create_chatbot(
        self,
        chatbot: dict,
        session: Depends
    ):
        new_chatbot = Chatbot(**chatbot)
        session.add(new_chatbot)
        session.commit()
        session.refresh(new_chatbot)
        return new_chatbot.__dict__
    
    async def get_chatbot_by_user_id(
        self,
        user_id: int,
        session: Depends
    ):
        chatbots = session.query(Chatbot).filter(Chatbot.user_id == user_id).order_by(Chatbot.updated_time.desc()).all()
        return chatbots

    async def get_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int,
        session: Depends
    ):
        chatbot = session.query(Chatbot).filter(Chatbot.id == chatbot_id).filter(Chatbot.user_id == user_id).first()
        return chatbot.__dict__
    
    async def get_chatbot_by_name(
        self,
        user_id: int,
        chatbot_name: str,
        session: Depends
    ):
        chatbots = session.query(Chatbot).filter(Chatbot.name == chatbot_name).filter(Chatbot.user_id == user_id).all()
        return [chatbot.__dict__ for chatbot in chatbots]

    async def update_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int,
        chatbot: dict,
        session: Depends
    ):
        chatbot_updated = session.query(Chatbot).filter(Chatbot.id == chatbot_id).filter(Chatbot.user_id == user_id)
        chatbot_updated.update(chatbot)
        session.commit()
        return chatbot_updated.all()
    
    async def update_time_by_id(
        self,
        chatbot_id: int,
        session: Depends
    ):
        chatbot_updated = session.query(Chatbot).filter(Chatbot.id == chatbot_id)
        chatbot_updated.update({"updated_time": datetime.now(timezone.utc).astimezone().isoformat()})
        session.commit()
        return [chatbot.__dict__ for chatbot in chatbot_updated.all()]
        
    
    async def delete_chatbot_by_id(
        self,
        user_id: int,
        chatbot_id: int,
        session: Depends
    ):
        chatbot_deleted = session.query(Chatbot).filter(Chatbot.id == chatbot_id).filter(Chatbot.user_id == user_id)
        if chatbot_deleted.first() == None:
            return []
        chatbot_deleted.delete()
        session.commit()
        return ['success']

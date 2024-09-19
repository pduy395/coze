from fastapi import Depends
from models.message import Message


class MessageDB:
    def __init__(self):
        pass

class MessageDBSupabase(MessageDB):
    def __init__(self):
        pass    

    async def get_message_by_chatbot_id(
        self,
        chatbot_id: int,
        start: int,
        end: int,
    ):
        messages = self.supabase.table("message").select("*").eq(
                        "chatbot_id", chatbot_id).order("time", desc=True).range(
                        start=start, end=end-1).execute().data
        return messages

    async def create_message(
        self,
        message: dict,
    ):
        created_message = self.supabase.table("message").insert(message).execute().data
        return created_message[0]
        return created_message[0]

    async def delete_message(
        self,
        message_id: int,
    ):
        deleted_message = self.supabase.table("message").delete().eq("id", message_id).execute().data
        return deleted_message

    async def delete_all_messages(
        self,
        chatbot_id: int,
    ):
        deleted_messages = self.supabase.table("message").delete().eq("chatbot_id", chatbot_id).execute().data
        return deleted_messages

    async def get_message_by_id(
        self,
        message_id: int,
    ):
        message = self.supabase.table("message").select("*").eq("id", message_id).execute().data
        return message[0]
    

class MessageDBPostgreSql(MessageDB):
    def __init__(self):
        pass

    async def get_message_by_chatbot_id(
        self,
        chatbot_id: int,
        start: int,
        end: int,
        session: Depends
    ):
        messages = session.query(Message)\
            .filter(Message.chatbot_id == chatbot_id)\
            .order_by(Message.time.desc())\
            .slice(start, end).all()
        return [message.__dict__ for message in messages]

    async def create_message(
        self,
        message: dict,
        session: Depends
    ):
        created_message = Message(**message)
        session.add(created_message)
        session.commit()
        session.refresh(created_message)
        return created_message.__dict__

    async def delete_message(
        self,
        message_id: int,
        session: Depends
    ):
        deleted_message = session.query(Message).filter(Message.id == message_id)
        deleted_message.delete()
        session.commit()
  
    async def delete_all_messages(
        self,
        chatbot_id: int,
        session: Depends
    ):
        deleted_messages = session.query(Message).filter(Message.chatbot_id == chatbot_id)
        deleted_messages.delete()
        session.commit()
         
    async def get_message_by_id(
        self,
        message_id: int,
        session: Depends
    ):
        message = session.query(Message).filter(Message.id == message_id).first()
        return message.__dict__
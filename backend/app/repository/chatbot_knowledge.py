from fastapi import Depends
from typing import List
from models.chatbot_knowledge import Chatbot_Knowledge


class ChatbotKnowledgeDB:
    def __init__(self) -> None:
        pass

    async def get_detail_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int
    ):
        pass

    async def get_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int,
    ):
        pass

    async def create_chatbot_knowledge(
        self,
        chatbot_knowledge: dict,
    ):
        pass

    async def delete_chatbot_knowledge(
        self,
        chatbot_id: int,
        knowledge_id: int,
    ):
        pass

    async def create_multi_chatbot_knowledge(
        self,
        chatbot_knowledges: List[dict],
    ):
        pass

    async def delete_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int,
    ):
        pass


class ChatbotKnowledgeDBSupabase(ChatbotKnowledgeDB):
    def __init__(self):
        pass

    async def get_detail_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int
    ):
        chatbot_knowledges = self.supabase.table("chatbot_knowledge").select("*", "knowledge(name)").eq("chatbot_id", chatbot_id).execute().data
        return chatbot_knowledges

    async def get_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int,
    ):
        chatbot_knowledges = self.supabase.table("chatbot_knowledge").select("*").eq("chatbot_id", chatbot_id).execute().data
        return chatbot_knowledges

    async def create_chatbot_knowledge(
        self,
        chatbot_knowledge: dict,
    ):
        chatbot_knowledge_created = self.supabase.table("chatbot_knowledge").insert(chatbot_knowledge).execute().data
        return chatbot_knowledge_created

    async def delete_chatbot_knowledge(
        self,
        chatbot_id: int,
        knowledge_id: int,
    ):
        chatbot_knowledge_deleted = self.supabase.table("chatbot_knowledge").delete().eq("chatbot_id", chatbot_id).eq("knowledge_id", knowledge_id).execute().data
        return chatbot_knowledge_deleted

    async def create_multi_chatbot_knowledge(
        self,
        chatbot_knowledges: List[dict],
    ):
        chatbot_knowledges_created = self.supabase.table("chatbot_knowledge").insert(chatbot_knowledges).execute().data
        return chatbot_knowledges_created

    async def delete_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int,
    ):
        chatbot_knowledge_deleted = self.supabase.table("chatbot_knowledge").delete().eq("chatbot_id", chatbot_id).execute().data
        return chatbot_knowledge_deleted


class ChatbotKnowledgeDBPostgreSql(ChatbotKnowledgeDB):
    def __init__(self, ):
        pass

    async def get_detail_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int,
        session: Depends
    ):
        chatbot_knowledges = session.query(Chatbot_Knowledge)\
            .filter(Chatbot_Knowledge.chatbot_id == chatbot_id)\
            .all()
        [chatbot_knowledge.knowledge for chatbot_knowledge in chatbot_knowledges]
        chatbot_knowledges = session.query(Chatbot_Knowledge)\
            .filter(Chatbot_Knowledge.chatbot_id == chatbot_id)\
            .all()
        [chatbot_knowledge.knowledge for chatbot_knowledge in chatbot_knowledges]
        return chatbot_knowledges

    async def get_chatbot_knowledge_by_chatbot_id(
        self,
        chatbot_id: int,
        session: Depends
    ):
        chatbot_knowledges = session.query(Chatbot_Knowledge).filter(Chatbot_Knowledge.chatbot_id == chatbot_id).all()
        return [chatbot_knowledge.__dict__ for chatbot_knowledge in chatbot_knowledges]

    async def create_chatbot_knowledge(
        self,
        chatbot_knowledge: dict,
        session: Depends
    ):
        chatbot_knowledge_created = Chatbot_Knowledge(**chatbot_knowledge)
        session.add(chatbot_knowledge_created)
        session.commit()
        return 'success'

    async def delete_chatbot_knowledge(
        self,
        chatbot_id: int,
        knowledge_id: int,
        session: Depends
    ):
        chatbot_knowledge_deleted = session.query(Chatbot_Knowledge)\
            .filter(Chatbot_Knowledge.chatbot_id == chatbot_id)\
            .filter(Chatbot_Knowledge.knowledge_id == knowledge_id)
        
        if chatbot_knowledge_deleted.first() == None:
            return []
        
        chatbot_knowledge_deleted.delete()
        session.commit()
        return ['success']
      

    async def create_multi_chatbot_knowledge(
        self,
        chatbot_knowledges: List[dict],
        session: Depends
    ):
        #chatbot_knowledges_created = self.supabase.table("chatbot_knowledge").insert(chatbot_knowledges).execute().data
        chatbot_knowledges_created = [Chatbot_Knowledge(**chatbot_knowledge) for chatbot_knowledge in chatbot_knowledges]
        session.add_all(chatbot_knowledges_created)
        session.commit()
        return chatbot_knowledges_created


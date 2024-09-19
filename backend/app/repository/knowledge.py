from fastapi import APIRouter, Depends, Security, HTTPException, status, UploadFile
from utils.exceptions import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from typing import Annotated, List
from schemas.knowledge import KnowledgeCreate, Knowledge_res
from .file import FileDB_postgresql
from datetime import datetime,timezone
from database.db_service import get_supabase, SessionLocal
from schemas import file
import models
from sqlalchemy import text
import json
from sqlalchemy import or_, and_
import schemas.file

file_db = FileDB_postgresql()



class KnowledgeDB():
    def __init__(self):
        pass
    async def check_dupicated_name(self, user_id,knowledge_name,knowledge_id):
        pass

    async def check_ownership(self, user_id,knowledge_id):
        pass

    async def update_time(self, user_id,knowledge_id):
        pass

    async def create_knowledge(self, knowledge: KnowledgeCreate, user_id):
        pass

    async def get_all(self, user_id):
        pass

    async def get_detail(self, user_id,knowledge_id):
        pass

    async def modify_knowledge(self, knowledge: KnowledgeCreate, knowledge_id):
        pass

    async def enable(self, user_id,enable:bool,knowledge_id):
        pass   

    async def get_embed_knowledge(self, knowledge_id):
        pass 

    async def get_search(self, knowledge_id,search):
        pass

    async def get_progress(self, knowledge_id):
        pass

    async def delete(self, user_id,knowledge_id):
        pass

    async def delete_embed(self, knowledge_id):
        pass


class KnowledgeDB_supabase(KnowledgeDB):
    def __init__(self):
        self.supabase = get_supabase()
        super().__init__()

    async def check_dupicated_name(self, user_id,knowledge_name,knowledge_id):
        try:
            res = self.supabase.table("knowledge").select("id").match({"user_id" : user_id,"name":knowledge_name}).execute().data
        except:
            raise BAD_REQUEST
        
        if res == [] or res[0]["id"] == knowledge_id:
            return
        if res != [] :
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Knowledge name duplicated")

    async def check_ownership(self, user_id,knowledge_id):
        try:
            res = self.supabase.table("knowledge").select("*").match({"user_id" : user_id,"id":knowledge_id}).execute().dict()["data"]
        except:
            raise BAD_REQUEST
        if res == []:
            raise NOT_FOUND
    
    async def update_time(self, user_id,knowledge_id):
        try:
            self.supabase.table("knowledge").update(
                {"edit_time":datetime.now(timezone.utc).astimezone().isoformat()}
            ).eq("id", knowledge_id).execute()
        except:
            raise BAD_REQUEST

    async def create_knowledge(
        self,
        knowledge: KnowledgeCreate, 
        user_id: int,
    ):
        res = self.supabase.table("knowledge").insert(
            {"description": knowledge.description,"name": knowledge.name, "user_id": user_id,"size":0,
                "icon":knowledge.icon,"enable":True,"format":knowledge.format,"edit_time":datetime.now(timezone.utc).astimezone().isoformat()}
        ).execute().data[0]
        return {"detail": "Knowledge created","id":res["id"]}

    async def get_all(
        self, 
        user_id: int,
    )-> List[Knowledge_res]:
        res = self.supabase.table("knowledge").select("id,name,edit_time,enable,icon,format,description,size, file(name),embed_type(type)").eq("user_id" , user_id).execute().dict()["data"]
        
        for i in range(len(res)):
            size =res[i]["size"]
            if size < 1024:
                res[i]["size"] = str(f"{size:.2f}") + " Byte"
            elif size <1024*1024:
                size = size/1024
                res[i]["size"] = str(f"{size:.2f}") + " KB"
            else :
                size = size/(1024*1024)
                res[i]["size"] = str(f"{size:.2f}") + " MB"

        return res
        


    async def get_detail(
        self, 
        user_id: int,
        knowledge_id:int
    ):
        document_count_res = (
            self.supabase.table("document")
            .select("id", count="exact")
            .eq("knowledge_id", knowledge_id)
            .execute()
        )

        # Lấy số lượng document từ kết quả
        document_count = document_count_res.dict()["count"]
        res = (
                self.supabase.table("knowledge")
                .select("id,name,edit_time,enable,icon,format,description,size, file(*),embed_type(*)")
                .eq("id", knowledge_id)
                .execute()
                .dict()["data"][0]
            )
        size =res["size"]
        if size < 1024:
            res["size"] = str(f"{size:.2f}") + " Byte"
        elif size <1024*1024:
            size = size/1024
            res["size"] = str(f"{size:.2f}") + " KB"
        else :
            size = size/(1024*1024)
            res["size"] = str(f"{size:.2f}") + " MB"
        return res,{"segment":document_count}


    async def modify_knowledge(
        self, 
        knowledge: KnowledgeCreate, 
        knowledge_id:int,
    ):
        res = self.supabase.table("knowledge").update(
            {"description": knowledge.description,"name": knowledge.name}
        ).eq("id", knowledge_id).execute()
        return {"detail": "updated"}


    async def enable( 
        self,    
        user_id: int,
        enable:bool,
        knowledge_id:int,
    ):    
        self.supabase.table("knowledge").update(
            {"enable": enable}
        ).eq("id", knowledge_id).execute()
        return {"detail": "updated"}

    async def get_embed_knowledge(
        self, 
        knowledge_id: int,
    ):
        res = self.supabase.table("document").select("content,file_id,index").match({"knowledge_id" : knowledge_id}).execute().data

        return res

    async def get_search(
            self, 
        knowledge_id: int,
        search
    ):
        res = self.supabase.table("document").select("content,file_id,index").match({"knowledge_id" : knowledge_id}).ilike("content",f"%\{search}%").execute().data

        return res

    async def get_progress(
            self, 
        knowledge_id: int,
    ):
        res = self.supabase.table("progress").select("file_id,progress").match({"knowledge_id" : knowledge_id}).execute().data
        return res

    async def delete(
        self, 
        user_id: int,
        knowledge_id:int
    ):
        self.supabase.table("document").delete().eq("knowledge_id", knowledge_id).execute()

        list_file = self.supabase.table("file").select("id").match({"knowledge_id" : knowledge_id}).execute().data
        
        for f in list_file:
            self.supabase.storage.from_("file").remove([f["id"]])
        self.supabase.table("file").delete().eq("knowledge_id", knowledge_id).execute()
        self.supabase.table("embed_type").delete().eq("knowledge_id", knowledge_id).execute()
        self.supabase.table("knowledge").delete().eq("id", knowledge_id).execute()
        return {"detail": "deleted"}

    
    async def delete_embed(
        self, 
        knowledge_id:int
    ):
        self.supabase.table("document").delete().eq("knowledge_id", knowledge_id).execute()
        self.supabase.table("embed_type").delete().eq("knowledge_id", knowledge_id).execute()
        return {"detail": "deleted"}
    

    async def insert_embed_type(self,
        type: file.Embed_type,
        knowledge_id:int,
        auto:bool,
    ):
        tmp = "Custom segmentation"
        if auto ==True:
            tmp = "Auto-segment"

        res = self.supabase.table("embed_type").insert(
            {"embed_model": type.embed_model,"knowledge_id":knowledge_id,
                "segment":type.segment,"max_length":type.max_length,
                "rule_1":type.rule_1,  "rule_2":type.rule_2,"type":tmp}
        ).execute()

    async def get_similarity_cosin(self,query_embedding,knowledge_ids):
        res = self.supabase.rpc('match_documents_4', {
        'query_embedding': query_embedding,
        'knowledge_ids': knowledge_ids
    }).execute().dict()["data"]
        return res
    


class KnowledgeDB_posgresql(KnowledgeDB):
    def __init__(self):
        super().__init__()
        # session = SessionLocal()
        self.supabase = get_supabase()

    async def check_dupicated_name(self, user_id,knowledge_name,knowledge_id,session: Depends):
        knowledge =session.query(models.knowledge.Knowledge).filter(and_(models.knowledge.Knowledge.user_id == user_id,
                                                                              models.knowledge.Knowledge.name == knowledge_name,
                                                                              models.knowledge.Knowledge.id != knowledge_id)).all()

        if knowledge != [] :
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Knowledge name duplicated")

    async def check_ownership(self, user_id,knowledge_id,session: Depends):
        knowledge =session.query(models.knowledge.Knowledge).filter(and_(models.knowledge.Knowledge.user_id == user_id,
                                                                              models.knowledge.Knowledge.id == knowledge_id)).first()

        if knowledge == None :
            raise NOT_FOUND
    
    async def update_time(self, user_id,knowledge_id,session: Depends):
        
        try:
            knowledge = session.query(models.Knowledge).filter(models.Knowledge.id == knowledge_id)
    
            knowledge.update({"edit_time":datetime.now(timezone.utc).astimezone().isoformat()})
            session.commit()
        except:
            raise BAD_REQUEST

    async def create_knowledge(
        self,
        knowledge: KnowledgeCreate, 
        user_id: int
        ,session: Depends
    ):
        new_knowledge = models.knowledge.Knowledge(icon = knowledge.icon, description= knowledge.description, format = knowledge.format,
                                                   name = knowledge.name,enable = True,user_id = user_id ,size =0,
                                                   edit_time = datetime.now(timezone.utc).astimezone().isoformat())
        session.add(new_knowledge)
        session.commit()
        session.refresh(new_knowledge)
        return {"detail": "Knowledge created","id":new_knowledge.id}
        

    async def get_all(
        self, 
        user_id,
        session: Depends
    ):
        knowledge = session.query(
        models.knowledge.Knowledge,
    ).filter(
        models.knowledge.Knowledge.user_id == user_id
    ).all()
        
        for i in range(len(knowledge)):
            # size =int(knowledge[i].size)
            # if size < 1024:
            #     knowledge[i].size = str(f"{size:.2f}") + " Byte"
            # elif size <1024*1024:
            #     size = size/1024
            #     knowledge[i].size = str(f"{size:.2f}") + " KB"
            # else :
            #     size = size/(1024*1024)
            #     knowledge[i].size = str(f"{size:.2f}") + " MB"
            knowledge[i].files 
            knowledge[i].embed_type 

        return knowledge
        


    async def get_detail(
        self, 
        user_id,
        knowledge_id:int,
        session: Depends
    ):
        document_res = session.query(
        models.document.Document,
    ).filter(
        models.document.Document.knowledge_id == knowledge_id
    ).all()

        # Lấy số lượng document từ kết quả
        document_count = len(document_res)
        res  = session.query(
        models.knowledge.Knowledge,
    ).filter(models.knowledge.Knowledge.id == knowledge_id
    ).first()
        res.files 
        res.embed_type 
        # size =int(res.size)
        # if size < 1024:
        #     res.size = str(f"{size:.2f}") + " Byte"
        # elif size <1024*1024:
        #     size = size/1024
        #     res.size = str(f"{size:.2f}") + " KB"
        # else :
        #     size = size/(1024*1024)
        #     res.size = str(f"{size:.2f}") + " MB"
        return res,{"segment":document_count}


    async def modify_knowledge(
        self, 
        knowledge: KnowledgeCreate, 
        knowledge_id:int
        ,session: Depends
    ):
        knowledge_db = session.query(models.Knowledge).filter(models.Knowledge.id == knowledge_id)
    
        knowledge_db.update({"description" : knowledge.description,"name": knowledge.name})
        session.commit()
        return {"detail": "knowledge updated"}


    async def enable( 
        self,    
        user_id: int,
        enable:bool,
        knowledge_id:int
        ,session: Depends
    ):  
        knowledge_db = session.query(models.Knowledge).filter(models.Knowledge.id == knowledge_id)
    
        knowledge_db.update({"enable": enable})
        session.commit()
        return {"detail": "knowledge updated"}  
        

    async def get_embed_knowledge(
        self, 
        knowledge_id: int
        ,session: Depends
    ):
        doc = session.query(models.Document.content,models.Document.file_id,models.Document.index).filter(models.Document.knowledge_id == knowledge_id).all()
        doc_contents = [{"content":d[0],"file_id": d[1],"index": d[2]} for d in doc]

    # Trả về danh sách các giá trị
        return doc_contents

    async def get_search(
            self, 
        knowledge_id: int,
        search
        ,session: Depends
    ):
        documents = session.query(models.Document.content,models.Document.file_id,models.Document.index).filter(
        models.Document.knowledge_id == knowledge_id,
        models.Document.content.ilike(f'%{search}%')
    ).all()
        
        doc_contents = [{"content":d[0],"file_id": d[1],"index": d[2]} for d in documents]

    # Trả về danh sách các giá trị
        return doc_contents
        

    async def get_progress(
            self, 
        knowledge_id: int
        ,session: Depends
    ):
        res = session.query(models.Progress).filter(models.Progress.knowledge_id == knowledge_id)
        return res

    async def delete(
        self, 
        user_id: int,
        knowledge_id:int
        ,session: Depends
    ):
        list_file = await file_db.get_list_file_id(knowledge_id,session)
        
        for id in list_file:
            self.supabase.storage.from_("file").remove([id])

        knowledge = session.query(models.Knowledge).filter(models.Knowledge.id == knowledge_id)
        knowledge.delete()
        session.commit()

        return {"detail": "deleted"}

    
    async def delete_embed(
        self, 
        knowledge_id:int
        ,session: Depends
    ):
        document = session.query(models.Document).filter(models.Document.knowledge_id == knowledge_id)
        document.delete()
        session.commit()

        embed_type = session.query(models.Embed_type).filter(models.Embed_type.knowledge_id == knowledge_id)
        embed_type.delete()
        session.commit()
        return {"detail": "deleted"}
    
    async def delete_embed_type(
        self, 
        knowledge_id:int,
        session: Depends
    ):
        embed_type = session.query(models.Embed_type).filter(models.Embed_type.knowledge_id == knowledge_id)
        embed_type.delete()
        session.commit()
        return 
    

    async def insert_embed_type(self,
        type: file.Embed_type,
        knowledge_id:int,
        auto:bool
        ,session: Depends
    ):
        tmp = "Custom segmentation"
        if auto ==True:
            tmp = "Auto-segment"

        new_embed_type = models.Embed_type(embed_model= type.embed_model,knowledge_id=knowledge_id,
                segment=type.segment,max_length=type.max_length,
                rule_1=type.rule_1,  rule_2=type.rule_2,type=tmp)
        session.add(new_embed_type)
        session.commit()
        session.refresh(new_embed_type)

    async def get_similarity_cosin(self,query_embedding,knowledge_ids,session: Depends):


        # print(query_embedding)
        # # Chuyển đổi list thành chuỗi JSON nếu cần
        query_embedding_str = json.dumps(query_embedding)
        # print(query_embedding_str)
        query = text("""
        SELECT * FROM match_documents_7(
            :query_embedding, 
            :knowledge_ids
        )
    """)
        response = session.execute(
            query,
            {
                'query_embedding': query_embedding_str,
                'knowledge_ids': knowledge_ids
            }
        ).fetchall()
        list_doc = []

        for r in response:
            list_doc.append({"content":r[0],"similarity":r[1],"file_id":r[2],"index":r[3]})
        return list_doc

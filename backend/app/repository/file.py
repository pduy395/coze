from fastapi import APIRouter, Depends, Security, UploadFile, HTTPException, status, BackgroundTasks
import schemas.file
from utils.exceptions import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from typing import List
import schemas
import models
from database.db_service import get_supabase, SessionLocal
from sqlalchemy import and_, or_


class FileDB():
    def __init__(self):
        pass

    async def check_ownership(self, user_id,file_id):
        pass

    async def check_embed(self, knowledge_id):
        pass

    async def get_list_file_id(self, knowledge_id):
        pass

    async def init_progress(self, knowledge_id,list_file_id):
        pass

    async def upload_file(self, user_id,knowledge_id,file_list: List[UploadFile],):
        pass
    
    async def upload_file_local(self, knowledge_id,content_type, temp_filename, file_name):
        pass

    async def rename(self, file_id,request: schemas.file.File_rename):
        pass


    async def get_embed_file(self, file_id,):
        pass

    async def get_search(self, file_id,search):
        pass

    async def get_link(self, file_id,):
        pass

    async def delete_file(self, file_id,knowledge_id):
        pass

class FileDB_supabase(FileDB):
    def __init__(self):
        super().__init__()
        self.supabase = get_supabase()
        
    
    async def check_ownership(self, user_id,file_id):
        try:
            knowledge_id = self.supabase.table("file").select("knowledge_id").match({"id" : file_id}).execute().dict()["data"][0]["knowledge_id"]
            res = self.supabase.table("knowledge").select("*").match({"user_id" : user_id,"id":knowledge_id}).execute().dict()["data"]    
        except:
            raise BAD_REQUEST
        if res ==[]:
            raise NOT_FOUND
        return knowledge_id

    async def check_embed(self, knowledge_id):
        try:
            type = self.supabase.table("embed_type").select("*").match({"knowledge_id": knowledge_id}).execute().data
        except:
            raise BAD_REQUEST
        if type !=[]:
            return type[0]
        else:
            return False
    
    async def get_list_file_id(
        self, 
        knowledge_id:int,
    ):
        list_file = self.supabase.table("file").select("id").match({"knowledge_id" : knowledge_id}).execute().data
        list_id = []
        for f in list_file:
            list_id.append(f["id"])
        return list_id

    async def init_progress(
        self, 
        knowledge_id:int, 
        list_file_id
    ):
        for id in list_file_id:
            res = self.supabase.table("progress").insert(
                {"knowledge_id": knowledge_id,"file_id":id,"progress":0}
            ).execute()

    def delete_progress(
        self, 
        knowledge_id, 
        file_id
    ):
        self.supabase.table("progress").delete().eq("file_id", file_id).eq("knowledge_id",knowledge_id).execute()   


    async def upload_file(
        self, 
        user_id:int,
        knowledge_id:int,
        file_list: List[UploadFile],
    ):
        list_id = []
        for file in file_list:
            f = await file.read()
            file_size = len(f)
            size = self.supabase.table("knowledge").select("size").match({"id": knowledge_id}).execute().data[0]["size"]
            res = self.supabase.table("knowledge").update(
                {"size": size + file_size,}
            ).eq("id", knowledge_id).execute()
            res = self.supabase.table("file").insert(
                {"name": file.filename,"knowledge_id":knowledge_id,"size":file_size}
            ).execute()
            file_id = res.data[0]['id']
            list_id.append(file_id)

            file_extension = file.filename.split(".")[-1].lower()
            if file_extension == "pdf":
                content_type = "application/pdf"
            elif file_extension == "txt":
                content_type = "text/plain"
            elif file_extension == "docx":
                content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unsupported file type",
                )
            self.supabase.storage.from_("file").upload(
                path= str(file_id), file=f, file_options={"content-type": content_type}
            )

        return {"list_id":list_id,"detail": "File upload"}

    async def upload_file_local(
        self, 
        knowledge_id:int,
        content_type, temp_filename, file_name):
        with open(temp_filename, 'rb') as file:
            file_content = file.read()

        file_size = len(file_content)
        size = self.supabase.table("knowledge").select("size").match({"id": knowledge_id}).execute().data[0]["size"]
        res = self.supabase.table("knowledge").update(
            {"size": size + file_size,}
        ).eq("id", knowledge_id).execute()

        res = self.supabase.table("file").insert(
            {"name": file_name,"knowledge_id":knowledge_id,"size":file_size}
        ).execute()
        file_id = res.data[0]['id']
        self.supabase.storage.from_("file").upload(path=str(file_id), file = file_content,file_options={"content-type": content_type})

        return file_id

    async def rename(
        self, 
        file_id: int,
        request: schemas.file.File_rename
    ):
        res = self.supabase.table("file").update(
            {"name": request.name}
        ).eq("id", file_id).execute()
        return {"detail": "updated"}
    

    async def get_embed_file(
        self,
        file_id: int,
    ):
        res = self.supabase.table("document").select("content,index").match({"file_id" : file_id}).order("index").execute().data
        return res

    async def get_search(
        self,
        file_id: int,
        search
    ):
        res = self.supabase.table("document").select("content,file_id,index").match({"file_id" : file_id}).order("index").ilike("content",f"%\{search}%").execute().data
        return res

    async def get_link(
        self,
        file_id: int,
    ):
        res = self.supabase.storage.from_("file").create_signed_url(
            path=str(file_id), expires_in=3600
        )
        return res


    # delete file
    async def delete_file(
        self, 
        file_id: int,
        knowledge_id:int
    ):
        file_size = self.supabase.table("file").select("size").match({"id" : file_id}).execute().data[0]["size"]
        self.supabase.storage.from_("file").remove([str(file_id)])
        self.supabase.table("document").delete().eq("file_id", file_id).execute()
        self.supabase.table("file").delete().eq("id", file_id).execute()

        size = self.supabase.table("knowledge").select("size").match({"id": knowledge_id}).execute().data[0]["size"]
        res = self.supabase.table("knowledge").update(
            {"size": size - file_size,}
        ).eq("id", knowledge_id).execute()
        
        return {"detail": "File deleted"}



class FileDB_postgresql(FileDB):
    def __init__(self):
        super().__init__()
        # self.session = SessionLocal()
        self.supabase = get_supabase()
        
    
    async def check_ownership(self, user_id,file_id,session: Depends):
        try:
            file = session.query(models.File,
            ).filter(models.File.id == file_id).first()
            if str(file.knowledge.user.id) == user_id:
                return str(file.knowledge.id)
            else:
                raise NOT_FOUND
        except:
            raise NOT_FOUND
        

    async def check_embed(self, knowledge_id,session: Depends):
        try:
            knowledge = session.query(models.Knowledge,
            ).filter(models.Knowledge.id == knowledge_id).first()
            if knowledge.embed_type == None:
                return False
            return knowledge.embed_type
        except:
            raise NOT_FOUND
    
    async def get_list_file_id(
        self, 
        knowledge_id:int,
        session: Depends
    ):
        list_id = []
        knowledge = session.query(models.Knowledge,
            ).filter(models.Knowledge.id == knowledge_id).first()
        for f in knowledge.files:
            list_id.append(f.id)
        return list_id

    async def init_progress(
        self, 
        knowledge_id:int, 
        list_file_id
        ,session: Depends
    ):
        for id in list_file_id:
            progress = session.query(models.Progress).filter(models.Progress.file_id == id)
            # if progress.first() != None:
            progress.delete()
            session.flush()


            new_progress = models.progress.Progress(knowledge_id = knowledge_id, file_id = id, progress = 0)
            session.add(new_progress)
            session.commit()
            # session.refresh(new_progress)

    def delete_progress(
        self, 
        knowledge_id, 
        file_id
    ):
        session = SessionLocal()
        try:
            progress = session.query(models.Progress).filter(models.Progress.file_id == file_id)
            progress.delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            session.close()

    def update_progress(
        self, 
        file_id,
        p,
        session: Depends
    ): 
        progress_db  = session.query(
                models.Progress,
                ).filter(models.Progress.file_id == file_id)

        progress_db.update({"progress": p})
        session.commit()


    async def upload_file(
        self, 
        user_id:int,
        knowledge_id:int,
        file_list: List[UploadFile]
        ,session: Depends
    ):
        list_id = []
        for file in file_list:
            f = await file.read()
            file_size = len(f)
            knowledge_db  = session.query(
            models.knowledge.Knowledge,
            ).filter(models.knowledge.Knowledge.id == knowledge_id)

            size = int(knowledge_db.first().size)
            knowledge_db.update({"size" : size + file_size})
            session.commit()

            new_file = models.File(name =  file.filename,knowledge_id = knowledge_id,size = file_size)
            session.add(new_file)
            session.commit()
            session.refresh(new_file)

            file_id = new_file.id
            list_id.append(file_id)

            file_extension = file.filename.split(".")[-1].lower()
            if file_extension == "pdf":
                content_type = "application/pdf"
            elif file_extension == "txt":
                content_type = "text/plain"
            elif file_extension == "docx":
                content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unsupported file type",
                )
            self.supabase.storage.from_("file").upload(
                path= str(file_id), file=f, file_options={"content-type": content_type}
            )

        return {"list_id":list_id,"detail": "File upload"}

    async def upload_file_local(
        self, 
        knowledge_id:int,
        content_type, temp_filename, file_name,
        session: Depends):

        with open(temp_filename, 'rb') as file:
            file_content = file.read()

        file_size = len(file_content)
        knowledge_db  = session.query(
            models.knowledge.Knowledge,
            ).filter(models.knowledge.Knowledge.id == knowledge_id)

        size = int(knowledge_db.first().size)
        knowledge_db.update({"size" : size + file_size})
        session.commit()

        new_file = models.File(name =  file_name,knowledge_id = knowledge_id,size = file_size)
        session.add(new_file)
        session.commit()
        session.refresh(new_file)
        file_id = new_file.id
        self.supabase.storage.from_("file").upload(path=str(file_id), file = file_content,file_options={"content-type": content_type})

        return file_id

    async def rename(
        self, 
        file_id: int,
        request: schemas.file.File_rename
        ,session: Depends
    ):
        file_db  = session.query(
        models.File,
        ).filter(models.File.id == file_id)

        file_db.update({"name": request.name})
        session.commit()

        return {"detail": "updated"}
    

    async def get_embed_file(
        self,
        file_id: int
        ,session: Depends
    ):
        doc = session.query(models.Document.content,models.Document.file_id,models.Document.index).filter(models.Document.file_id == file_id).order_by(models.Document.index).all()
        doc_contents = [{"content":d[0],"file_id": d[1],"index": d[2]} for d in doc]

        # Trả về danh sách các giá trị
        return doc_contents
    
    async def get_text_file(
        self,
        file_id: int
        ,session: Depends
    ):
        doc = session.query(models.Document.content,models.Document.file_id,models.Document.index).filter(models.Document.file_id == file_id).order_by(models.Document.index).all()
        # doc_contents = [{"content":d[0],"file_id": d[1],"index": d[2]} for d in doc]
        doc_contents = ""
        for d in doc:
            doc_contents = doc_contents + d[0] + "\n"

        return doc_contents
    
    async def delete_segment_file(
        self,
        file_id: int
        ,session: Depends
    ):
        document = session.query(models.Document).filter(models.Document.file_id == file_id)
        document.delete()
        session.commit()

    async def get_search(
        self,
        file_id: int,
        search
        ,session: Depends
    ):
        doc = session.query(models.Document.content,models.Document.file_id,models.Document.index
                                 ).filter(models.Document.file_id == file_id,
                                            models.Document.content.ilike(f'%{search}%')).order_by(models.Document.index).all()
        doc_contents = [{"content":d[0],"file_id": d[1],"index": d[2]} for d in doc]
        return doc_contents

    async def get_link(
        self,
        file_id: int
        ,session: Depends
    ):
        res = self.supabase.storage.from_("file").create_signed_url(
            path=str(file_id), expires_in=3600
        )
        return res


    # delete file
    async def delete_file(
        self, 
        file_id: int,
        knowledge_id:int
        ,session: Depends
    ):
        file_size = session.query(models.File).filter(models.File.id == file_id).first().size
        file_size = int(file_size)
        knowledge_db  = session.query(
            models.knowledge.Knowledge,
            ).filter(models.knowledge.Knowledge.id == knowledge_id)

        size = int(knowledge_db.first().size)
        knowledge_db.update({"size" : size - file_size})
        session.commit()

        self.supabase.storage.from_("file").remove([str(file_id)])

        file = session.query(models.File).filter(models.File.id == file_id)
        file.delete()
        session.commit()

        progress = session.query(models.Progress).filter(models.Progress.file_id == file_id)
        progress.delete()
        session.commit()
        
        return {"detail": "File deleted"}

    async def enrich_context(
        self, 
        file_id: int,
        start:int,
        end:int,
        session: Depends
    ):
        content = ""
        for i in range(start,end+1):
            tmp = session.query(models.Document.content).filter(and_(models.Document.file_id == file_id,models.Document.index == i)).first()
            if tmp != None:
                content = content + "\n" + str(tmp.content)
        return content

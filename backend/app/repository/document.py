from database.db_service import get_supabase, SessionLocal
from fastapi import Depends
from utils.embedding import split_docs
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
import models
from sqlalchemy import text
from sqlalchemy import or_, and_



class DocumentDB():
    def __init__(self):
        pass

    async def insert_doc(self, embedding,knowledge_id,file_id,doc,index):   
        pass  

    async def replace_doc(self,embedding,file_id,doc,index):
        pass  

    def embed_doc(self, file_id, knowledge_id, doc, doc_metadata,embedding,i,l):
        pass

class DocumentDB_supabase(DocumentDB):
    def __init__(self):
        super().__init__()
        self.supabase = get_supabase()

    async def insert_doc(self,embedding,knowledge_id,file_id,doc,index):  
        response = self.supabase.rpc('update_document_indices', {
                'f_id': file_id,
                'i': index
            }).execute()   
        
        response = self.supabase.table("document").insert({
            'file_id': file_id,
            'knowledge_id':knowledge_id,
            'content': doc,
            'meta_data': "doc_metadata",
            'vector': embedding,
            'index':index
        }).execute()
        return {"detail": "successfully insert"}

    async def replace_doc(self,embedding,file_id,doc,index):  
        response = self.supabase.table("document").update({"content": doc,"vector": embedding}).eq("index", index).eq("file_id", file_id).execute()
        return {"detail": "successfully update"}
    
    def embed_doc(self, file_id, knowledge_id, doc, doc_metadata,embedding,i,l):

        response = self.supabase.table("document").insert({
            'file_id': file_id,
            'knowledge_id':knowledge_id,
            'content': doc.page_content,
            'meta_data': doc_metadata,
            'vector': embedding,
            'index':i
        }).execute()
        
        self.supabase.table("progress").update({"progress": round(i/l*100)}).eq("file_id", file_id).eq("knowledge_id",knowledge_id).execute()
        print(round(i/l*100))


class DocumentDB_posgresql(DocumentDB):
    def __init__(self):
        super().__init__()
        # self.session = SessionLocal()

    async def insert_doc(self,embedding,knowledge_id,file_id,doc,index,session: Depends): 
        response = session.execute(
                    text("SELECT update_document_indices(:f_id, :i)"),
                    {'f_id': file_id, 'i': index}
                ).fetchall()

        new_doc = models.Document( 
            file_id= file_id,
            knowledge_id= knowledge_id,
            content= doc,
            meta_data= "doc_metadata",
            vector= embedding,
            index= index)
        session.add(new_doc)
        session.commit()
        session.refresh(new_doc)
        
        return {"detail": "successfully insert"}

    async def replace_doc(self,embedding,file_id,doc,index,session: Depends):  
        doc_db  = session.query(
        models.Document,
        ).filter(and_(models.Document.file_id == file_id,models.Document.index == index))
        print(file_id,index)
        doc_db.update({"content": doc,"vector": embedding})
        session.commit()
        return {"detail": "successfully update"}
    
    def embed_doc(self, file_id, knowledge_id, doc, doc_metadata,embedding,i,l):
        session = SessionLocal()
        try:
            new_doc = models.Document( 
                file_id= file_id,
                knowledge_id= knowledge_id,
                content= doc.page_content,
                meta_data= doc_metadata,
                vector= embedding,
                index= i)
            session.add(new_doc)
            session.commit()
            session.refresh(new_doc)

            progress_db  = session.query(
                models.Progress,
                ).filter(and_(models.Progress.file_id == file_id, models.Progress.knowledge_id == knowledge_id))

            progress_db.update({"progress": round(i/l*100)})
            session.commit()
            # print(round(i/l*100))
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
            e_session = SessionLocal()
            try:
                progress = e_session.query(models.Progress).filter(models.Progress.file_id == file_id)
                progress.delete()
                e_session.commit()
            except Exception as e:
                e_session.rollback()
            finally:
                e_session.close()
        finally:
            session.close()

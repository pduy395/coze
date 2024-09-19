from schemas import file
import concurrent
import concurrent.futures
from repository.file import FileDB_supabase, FileDB_postgresql
from repository.document import DocumentDB_supabase, DocumentDB_posgresql
from repository.knowledge import KnowledgeDB_supabase, KnowledgeDB_posgresql
from sentence_transformers import SentenceTransformer
from service.embedding import get_embedding
from dotenv import load_dotenv
from utils.embedding import split_docs, extract_text_from_file, split_docs_from_text
from fastapi import Depends, HTTPException, status
import gc
import torch
import os
import glob
from fastapi import Depends

executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

file_db = FileDB_postgresql()
document_db = DocumentDB_posgresql()
knowledge_db = KnowledgeDB_posgresql()

def insert_documents_with_file_id(docs, file_id, knowledge_id,document_db,file_db):
    i=0
    l=len(docs)
    for doc in docs: 
        # sentences_tokenizer = tokenize(doc.page_content)
        embedding = get_embedding(doc.page_content)
        doc_metadata = doc.metadata 
        i = i+1
        document_db.embed_doc(file_id,knowledge_id,doc,doc_metadata,embedding,i,l)
        
    file_db.delete_progress(knowledge_id,file_id)


def embedding_file(text,file_id,knowledge_id,segment, max_segment_length,rule_1,rule_2,embed_model,document_db,file_db,session: Depends):
    try:
        docs = split_docs_from_text(text,segment,max_segment_length,rule_1,rule_2,knowledge_id)
    except Exception as e:
        try:
            file_db.update_progress(file_id,-1,session)

            directory = ''
            files = glob.glob(os.path.join(directory, 'temp*'))
            for file in files:
                os.remove(file)
    
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.args,
                )
        
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.args,
                )
         
    try:
        insert_documents_with_file_id(docs,file_id,knowledge_id,document_db,file_db)
    except Exception as e:
        print(e.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= e.args )
        
    return 




async def embed_first(
        type: file.Embed_type,
        knowledge_id:int,
        auto:bool,
        session: Depends
    ):  
        await knowledge_db.insert_embed_type(type,knowledge_id,auto,session)
        list_file = await file_db.get_list_file_id(knowledge_id,session)
        futures = []
        for file_id in list_file:

            url = await file_db.get_link(file_id,session)
            url = url["signedURL"]
            try:
                text  = extract_text_from_file(url)
            except Exception as e:
                try:
                    file_db.update_progress(file_id,-1,session)

                    directory = ''
                    files = glob.glob(os.path.join(directory, 'temp*'))
                    for file in files:
                        os.remove(file)
                    continue
                except:
                    continue

            future = executor.submit(embedding_file,
                            text,
                            file_id,
                            knowledge_id,
                            type.segment, 
                            type.max_length,
                            type.rule_1,
                            type.rule_2,
                            type.embed_model,
                            document_db,
                            file_db,
                            session)

            futures.append(future)
        return {"detail": "File embeded"}

async def re_embed(
        type: file.Embed_type,
        knowledge_id:int,
        auto:bool,
        session: Depends
    ):  
        await knowledge_db.delete_embed_type(knowledge_id,session)
        await knowledge_db.insert_embed_type(type,knowledge_id,auto,session)

        list_file = await file_db.get_list_file_id(knowledge_id,session)
        res = await knowledge_db.get_progress(knowledge_id,session)
        for r in res:
            if int(r.progress) == -1:
                list_file.remove(int(r.file_id))
        print(list_file)
            
        futures = []
        for file_id in list_file:
            text = await file_db.get_text_file(file_id,session)
            print("*")
            await file_db.delete_segment_file(file_id,session)

            future = executor.submit(embedding_file,
                            text,
                            file_id,
                            knowledge_id,
                            type.segment, 
                            type.max_length,
                            type.rule_1,
                            type.rule_2,
                            type.embed_model,
                            document_db,
                            file_db,
                            session)

            futures.append(future)
        return {"detail": "File embeded"}


async def embed_next(
    file_id_list,
    knowledge_id,
    type,
    session: Depends
):
    
    futures = []
    for file_id in file_id_list:
        url = await file_db.get_link( file_id,session)
        url = url["signedURL"]

        try:
            text  = extract_text_from_file(url)
        except Exception as e:
            try:
                file_db.update_progress(file_id,-1,session)

                directory = ''
                files = glob.glob(os.path.join(directory, 'temp*'))
                for file in files:
                    os.remove(file)
                continue
            except:
                continue

        future = executor.submit(embedding_file,
                                    text,
                                    file_id,
                                    knowledge_id,
                                    type.segment, 
                                    type.max_length,
                                    type.rule_1,
                                    type.rule_2,
                                    type.embed_model,
                                    document_db,
                                    file_db,
                                    session)

        futures.append(future)
    # concurrent.futures.wait(futures)

    return {"detail": "File embeded"}



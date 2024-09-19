from fastapi import APIRouter, Depends, Security, UploadFile, HTTPException, status, FastAPI, BackgroundTasks
import schemas.file
from typing import Annotated
from utils.JWTtoken import get_id
from repository.file import FileDB_supabase, FileDB_postgresql
from repository.knowledge import KnowledgeDB_supabase, KnowledgeDB_posgresql
from repository.document import DocumentDB_supabase, DocumentDB_posgresql
from langchain_huggingface import HuggingFaceEmbeddings
import schemas
from utils.exceptions import BAD_REQUEST
from typing import List
import uuid
import os
from service import document
from sqlalchemy.orm import Session
from database.db_service import get_postgresql
from utils.get_data_from_url import create_thread_get_data, get_file_lock
import torch
import gc
import json
import glob
from sentence_transformers import SentenceTransformer
from service.embedding import get_embedding

# model = SentenceTransformer('pkshatech/GLuCoSE-base-ja', device='cpu')

file_db = FileDB_postgresql()
knowledge_db =  KnowledgeDB_posgresql()
document_db = DocumentDB_posgresql()
file_db = FileDB_postgresql()
knowledge_db =  KnowledgeDB_posgresql()
document_db = DocumentDB_posgresql()

router = APIRouter(tags=["File"], prefix='/file')


@router.post("",status_code=status.HTTP_200_OK )
async def upload_file(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id:int,
    request: List[UploadFile],
    session: Session = Depends(get_postgresql)
):
    for r in request:
        valid_extensions = ["pdf", "docx","txt"]
        file_extension = r.filename.split(".")[-1].lower()

        if file_extension not in valid_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF, DOCX or TXT files are accepted",
            )
    
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    await knowledge_db.update_time(user_id,knowledge_id,session)
    try:
        return await file_db.upload_file(user_id,knowledge_id,request,session)
    except Exception as e:
        return  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )





@router.put("/data_url",status_code=status.HTTP_200_OK )
async def get_data_url(
    user_id: Annotated[str, Security(get_id)],
    request: List[schemas.file.UploadURL],
):
    
    try:
        directory = ''
        files = glob.glob(os.path.join(directory, str(user_id) + '*'))
        for file in files:
            os.remove(file)

        create_thread_get_data(user_id,request)
        return {"detail":"processing"}
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

@router.get("/data_url",status_code=status.HTTP_200_OK )
async def get_data_from_local(
    user_id: Annotated[str, Security(get_id)],
):

    directory = ''
    files = glob.glob(os.path.join(directory, str(user_id) + '*'))
    list_data = []
    delete_list = []
    for file in files:

        # file_lock = get_file_lock(file)
        # if file_lock.locked():
        #      print("block_read")
        #      list_data.append({})
        # else:
        #     print("read")
        #     with file_lock:
        #         print("allow_read")
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            list_data.append(data)
            if data != {}:
                delete_list.append(file)

    for file in delete_list:
        os.remove(file)
    
    return list_data



@router.post("/data_url",status_code=status.HTTP_200_OK )
async def up_data_url(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id:int,
    request: List[schemas.file.url_data],
    session: Session = Depends(get_postgresql)
):   
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    await knowledge_db.update_time(user_id,knowledge_id,session)

    try:
        list_id = []
        uuid4 = uuid.uuid4()
        for r in request:
            file_name = str(uuid4) + ".txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(r.content)
            id  = await file_db.upload_file_local(knowledge_id,"text/plain",file_name,r.name,session)
            list_id.append(id)
            os.remove(file_name)
        return {"list_id":list_id,"detail": "Upload"}
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

    



@router.put("/{file_id}/name",status_code=status.HTTP_202_ACCEPTED)
async def re_name(
    user_id: Annotated[str, Security(get_id)],
    file_id: int,
    request: schemas.file.File_rename,
    session: Session = Depends(get_postgresql)
):
    await file_db.check_ownership(user_id,file_id,session)
    try:
        return await file_db.rename(file_id,request,session)
    except Exception as e:
        return  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    
@router.put("/{knowledge_id}/embed-first",status_code=status.HTTP_202_ACCEPTED )
async def embed_first(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id: int,
    type: schemas.file.Embed_type,
    auto:bool,
    session: Session = Depends(get_postgresql)
):    
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    print("1")
    check = await file_db.check_embed(knowledge_id,session)
    print("2")
    if check !=False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="file was set embed type")
    try:
        list_id = await file_db.get_list_file_id(knowledge_id,session)
        print("2")
        print(list_id)
        await file_db.init_progress(knowledge_id,list_id,session)
        print("3")
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    print("4")
    if auto ==True:
        type.embed_model="simCSE"
        type.segment = "\n"
        type.max_length = 500
        type.rule_1 = 1
        type.rule_2 = 1
    try:
        return await document.embed_first(type,knowledge_id,auto,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    
@router.put("/embed-next",status_code=status.HTTP_202_ACCEPTED, )
async def embed_next(
    user_id: Annotated[str, Security(get_id)],
    file_id_list: List[int],
    session: Session = Depends(get_postgresql)
):
    for file_id in file_id_list:
        knowledge_id = await file_db.check_ownership(user_id,file_id,session)
    type = await file_db.check_embed(knowledge_id,session)
    if type ==False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="file wasn't set embed type")
    try:
        await file_db.init_progress(knowledge_id,file_id_list,session)
        return await document.embed_next(file_id_list,knowledge_id,type,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    

@router.get("/{file_id}/embed",status_code=status.HTTP_200_OK )
async def get_embed_file(
    user_id: Annotated[str, Security(get_id)],
    file_id: int,
    offset: int = 0,
    limit: int = 10,
    search:str = "",
    session: Session = Depends(get_postgresql)
):
    await file_db.check_ownership(user_id,file_id,session)
    try:
        if search == "":
            res = await file_db.get_embed_file(file_id,session)
        else:
            res = await file_db.get_search(file_id,search,session)
        paginated_res = res[offset:offset + limit]
        return paginated_res
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

# # get url of file from supabase storage
# @router.get("/{file_id}/link",status_code=status.HTTP_200_OK, description="Get url of file")
# async def get_link(
#     user_id: Annotated[str, Security(get_id)],
#     file_id: int,
# ):
#     await file.check_ownership(supabase,user_id,file_id)
#     try:
#         return await file.get_link(supabase,file_id)
#     except Exception as e:
#         raise  HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=e.args,
#         )
    

@router.put("/replace-doc",status_code=status.HTTP_202_ACCEPTED)
async def replace_doc(
    user_id: Annotated[str, Security(get_id)],
    file_id: int,
    index:int,
    doc:schemas.file.Document,
    session: Session = Depends(get_postgresql)
):
    await file_db.check_ownership(user_id,file_id,session)
    try:
        

        embedding = get_embedding(doc.content)
        gc.collect()
        torch.cuda.empty_cache()
        return await document_db.replace_doc(embedding,file_id,doc.content,index,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )


@router.put("/insert-doc",status_code=status.HTTP_202_ACCEPTED)
async def insert_doc(
    user_id: Annotated[str, Security(get_id)],
    file_id: int,
    index:int,
    doc:schemas.file.Document,
    session: Session = Depends(get_postgresql)
):
    knowledge_id = await file_db.check_ownership(user_id,file_id,session)
    try:
        embedding = get_embedding(doc.content)
        gc.collect()
        torch.cuda.empty_cache()
        return await document_db.insert_doc(embedding,knowledge_id,file_id,doc.content,index,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )


# delete file
@router.delete("",description="Delete file")
async def delete_file(
    user_id: Annotated[str, Security(get_id)],
    file_id: int,
    session: Session = Depends(get_postgresql)
):
    knowledge_id = await file_db.check_ownership(user_id,file_id,session)
    await knowledge_db.update_time(user_id,knowledge_id,session)
    try:
        return await file_db.delete_file(file_id,knowledge_id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

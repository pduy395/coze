from fastapi import APIRouter, Depends, Security, UploadFile, HTTPException,status
from typing import Annotated, List
from utils.JWTtoken import get_id
from schemas.knowledge import KnowledgeCreate, Knowledge_res
from repository.knowledge import KnowledgeDB_supabase, KnowledgeDB_posgresql
from repository.file import FileDB_postgresql, FileDB_supabase
from langchain_huggingface import HuggingFaceEmbeddings
from database.db_service import get_postgresql
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
import schemas.file
from service import document


knowledge_db = KnowledgeDB_posgresql()
file_db = FileDB_postgresql()



router = APIRouter(tags=["Knowledge"], prefix='/knowledge')

@router.post("",status_code=status.HTTP_201_CREATED)
async def create_knowledge(
    request: KnowledgeCreate, 
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    await knowledge_db.check_dupicated_name(user_id,request.name,-1,session)
    try:
        return await knowledge_db.create_knowledge(request,user_id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

@router.get("/all",status_code=status.HTTP_200_OK)
async def get_all(
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        return await knowledge_db.get_all(user_id,session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

@router.get("/{knowledge_id}",status_code=status.HTTP_200_OK)
async def get_detail(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id: int,
    session: Session = Depends(get_postgresql)
):
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        return await knowledge_db.get_detail(user_id,knowledge_id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )


@router.put("/{knowledge_id}/modify",status_code=status.HTTP_202_ACCEPTED,)
async def modify_knowledge(
    request: KnowledgeCreate, 
    knowledge_id:int,
    user_id: Annotated[str, Security(get_id)],
    session: Session = Depends(get_postgresql)
):
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    await knowledge_db.check_dupicated_name(user_id,request.name,knowledge_id,session)
    await knowledge_db.update_time(user_id,knowledge_id,session)
    try:
        return await knowledge_db.modify_knowledge(request,knowledge_id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

from service.retrieval import get_similarity_document

@router.patch("/retrieval",status_code=status.HTTP_200_OK )
async def get(
    user_id: Annotated[str, Security(get_id)],
    knowledge_ids:List[int],
    input:str,
    session: Session = Depends(get_postgresql)
):  
    for knowledge_id in knowledge_ids:
        await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        model = SentenceTransformer('pkshatech/GLuCoSE-base-ja').to('cpu')
        return await get_similarity_document(knowledge_ids,input,session,model)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    

@router.put("/{knowledge_id}/enable",status_code=status.HTTP_202_ACCEPTED,)
async def enable(
    user_id: Annotated[str, Security(get_id)],
    request:bool,
    knowledge_id: int,
    session: Session = Depends(get_postgresql)
):  
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        return await knowledge_db.enable(user_id,request,knowledge_id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    

@router.get("/{knowledge_id}/embed", status_code=status.HTTP_200_OK)
async def get_embed_file(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id: int,
    offset: int = 0,
    limit: int = 10,
    search: str = "",
    session: Session = Depends(get_postgresql)
):
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        if search == "":
            res = await knowledge_db.get_embed_knowledge(knowledge_id,session)
        else:
            res = await knowledge_db.get_search(knowledge_id,search,session)
        sorted_documents = sorted(res, key=lambda x: (x['file_id'], x['index']))
        paginated_res = sorted_documents[offset: offset + limit]
        return paginated_res
        
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )


# delete knowledge
@router.delete("/{knowledge_id}", description="Delete knowledge")
async def delete_knowledge(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id: int,
    session: Session = Depends(get_postgresql)
):
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        return await knowledge_db.delete(user_id,knowledge_id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    
# delete knowledge
@router.delete("/{knowledge_id}/segment", description="Delete knowledge segment")
async def delete_knowledge(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id: int,
    session: Session = Depends(get_postgresql)
):
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        return await knowledge_db.delete_embed(knowledge_id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    
@router.post("/{knowledge_id}/resegment", description="Resegment knowledge")
async def resegment_knowledge(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id: int,
    type: schemas.file.Embed_type,
    auto:bool,
    session: Session = Depends(get_postgresql),
):
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        list_id = await file_db.get_list_file_id(knowledge_id,session)
        res = await knowledge_db.get_progress(knowledge_id,session)
        for r in res:
            print(int(r.file_id))
            list_id.remove(int(r.file_id))
        print(list_id)
        await file_db.init_progress(knowledge_id,list_id,session)
         
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    
    if auto ==True:
        type.embed_model="simCSE"
        type.segment = "\n"
        type.max_length = 500
        type.rule_1 = 1
        type.rule_2 = 1
    try:
        return await document.re_embed(type,knowledge_id,auto,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
    
@router.get("/{knowledge_id}/progress",status_code=status.HTTP_200_OK)
async def get_progress(
    user_id: Annotated[str, Security(get_id)],
    knowledge_id: int,
    session: Session = Depends(get_postgresql)
):
    await knowledge_db.check_ownership(user_id,knowledge_id,session)
    try:
        res_json = {}
        res =await knowledge_db.get_progress(knowledge_id,session)
        for r in res:
            res_json[str(r.file_id)] = (r.progress)
        print(res_json)
        return res_json
        
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )
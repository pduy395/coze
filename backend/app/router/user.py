from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from supabase import Client
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import  OAuth2PasswordRequestForm
from schemas.user import User, UserUpdate, ChangePassword, UserShow
import schemas.user
from utils.JWTtoken import get_id, oauth2_scheme
import schemas.user
from utils.JWTtoken import get_id, oauth2_scheme
from gotrue.errors import AuthApiError
from repository.user import UserDB_supabase, UserDB_posgresql
import schemas
from database.db_service import get_postgresql

user_db = UserDB_posgresql()



router = APIRouter(tags=["User"],prefix="/user")

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_user(
    request: User, 
    session: Session = Depends(get_postgresql)
):
    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password should be at least 6 characters",
        )
    try:
        return await user_db.register_user(request,session)
    except Exception as e:
        raise  e


    

    
@router.post("/login",status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_postgresql)
):
    email = form_data.username
    password = form_data.password
    try:
        return await user_db.login(email,password,session)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )


@router.get("",response_model=schemas.user.UserShow,status_code=status.HTTP_200_OK)
async def get_user_info(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_postgresql)
):
    try:
        return await user_db.get_user_info(token,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )


@router.put("/info",response_model=schemas.user.UserShow,status_code=status.HTTP_202_ACCEPTED, description="Update user info")
async def update_user_info(
    new_user_info: UserUpdate,
    id: Annotated[str, Depends(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        return await user_db.update_user_info(new_user_info,id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )



@router.put("/password",status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    change: ChangePassword,
    user_id: Annotated[str, Depends(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        return await user_db.change_password(change,user_id,session)
    except Exception as e:
        raise e



@router.put("/avatar",status_code=status.HTTP_202_ACCEPTED)
async def create_upload_file(
    file: UploadFile,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_postgresql)
):  
    if file.content_type != "image/jpeg":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only jpg file is accepted",
        )
    try:
        return await user_db.create_upload_file(file,token,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )


@router.delete("", description="Delete user")
async def delete(
    id: Annotated[str, Depends(get_id)],
    session: Session = Depends(get_postgresql)
):
    try:
        return await user_db.delete_user(id,session)
    except Exception as e:
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args,
        )

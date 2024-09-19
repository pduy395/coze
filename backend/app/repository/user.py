from fastapi import APIRouter, Depends, HTTPException,  status, UploadFile, Security
from fastapi.encoders import jsonable_encoder
from database.db_service import get_supabase, SessionLocal
import models.user
from schemas.user import User, UserShow, UserUpdate, ChangePassword
from utils.auth import get_user_response
import re
import models
import schemas
from utils import hashing
from datetime import datetime, timedelta
from utils.JWTtoken import get_id
from utils import JWTtoken
from .file import FileDB_postgresql

file_db = FileDB_postgresql()


def replace_ip(url, old_ip, new_ip):
    return re.sub(rf'\b{old_ip}\b', new_ip, url)


class UserDB():
    def __init__(self):
        pass

    async def register_user(self, user: User):
        pass

    async def login(self, email, password):
        pass

    async def get_user_info(self, token):
        pass
    
    async def update_user_info(self, new_user_info: UserUpdate,id):
        pass

    async def change_password(self, change:ChangePassword,user_id):
        pass

    async def create_upload_file(self, file: UploadFile,token: str): 
        pass 

    async def delete_user(self, id):
        pass




class UserDB_supabase(UserDB):
    def __init__(self):
        super().__init__()
        self.supabase = get_supabase()

    async def register_user(self, user: User):  
        res = self.supabase.auth.sign_up(
            {
                "email": user.mail,
                "password": user.password,
                "options": {
                    "data": jsonable_encoder(user, exclude=("password", "email"))
                },
            }
        )
        return {"detail": "User created"}
    

    async def login(self, email, password):
        user = self.supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        old_ip = "127.0.0.1"
        new_ip = "192.168.1.7"
        user.session.user.user_metadata["avatar"] = replace_ip(user.session.user.user_metadata["avatar"], old_ip, new_ip)
        
        return {
            "access_token": user.session.access_token,
            "token_type": "bearer",
            "data":user.session.user.user_metadata
        }


    async def get_user_info(self, token,):
        user_response = await get_user_response(token, self.supabase)
        old_ip = "127.0.0.1"
        new_ip = "192.168.1.7"
        url = user_response.user.user_metadata["avatar"]
        new_url = replace_ip(url, old_ip, new_ip)
        return {'username':user_response.user.user_metadata["username"],'mail':user_response.user.user_metadata["mail"],'avatar':new_url,'alias':user_response.user.user_metadata["alias"],'personal_signature':user_response.user.user_metadata["personal_signature"]}


    async def update_user_info(self, new_user_info: UserUpdate,id: int):
        res = self.supabase.auth.admin.update_user_by_id(id,{ 'user_metadata': { 'username':new_user_info.username,'alias':new_user_info.alias,'personal_signature':new_user_info.personal_signature } })
        
        return {"username": res.user.user_metadata["username"],"personal_signature": res.user.user_metadata["personal_signature"],"alias": res.user.user_metadata["alias"],"detail": "successfully updated"}

    async def change_password(self,change:ChangePassword,user_id):
        NewPass = change.new_pass
        OldPass = change.old_password
        # res = supabase.auth.admin.update_user_by_id(user_id,{ 'password': password })
        data = self.supabase.rpc('changepassword',{'current_plain_password': OldPass, 'new_plain_password': NewPass, 'current_id': user_id}).execute()
        return data.data 

    async def create_upload_file(self, file: UploadFile,token: str):  
        user = self.supabase.auth.get_user(token).user
        f = await file.read()
        if user.user_metadata['avatar'] == "https://i.sstatic.net/l60Hf.png":
            self.supabase.storage.from_("avatar").upload(
            path=f'avatar_{user.id}', file=f, file_options={"content-type": "image/jpeg"}
            )
        else:
            self.supabase.storage.from_("avatar").remove([f'avatar_{user.id}'])
            self.supabase.storage.from_("avatar").upload(
            path=f'avatar_{user.id}', file=f, file_options={"content-type": "image/jpeg"}
            )

        url = self.supabase.storage.from_('avatar').create_signed_url(path=f'avatar_{user.id}', expires_in=30000000)["signedURL"]
        res = self.supabase.auth.admin.update_user_by_id(user.id,{ 'user_metadata': { 'avatar': url } })

        return {"url":url,"detail": "successfully upload"}

    async def delete_user(self, id):
        res = self.supabase.auth.admin.delete_user(id)
        return {"detail": "successfully delete"}


class UserDB_posgresql(UserDB):
    def __init__(self):
        super().__init__()
        # session = SessionLocal()
        self.supabase = get_supabase()

    async def register_user(self, user: User,session: Depends):  
        res = session.query(models.user.User).filter(models.user.User.mail == user.mail).first()
        if res:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email is existed")

        new_user = models.user.User(username = user.username,avatar = user.avatar,alias = user.alias,personal_signature = user.personal_signature, mail = user.mail, password = hashing.Hash.bcrypt(user.password))
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"detail": "successfully sign up"}
    

    async def login(self, email, password,session: Depends):
        user = session.query(models.User).filter(models.User.mail == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='not exist account')
        
        if not hashing.Hash.verify(user.password, password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='incorrect password')


        access_token_expires = timedelta(minutes= JWTtoken.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = JWTtoken.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


    async def get_user_info(self, token,session: Depends):
        user = session.query(models.User).filter(models.User.id == get_id(token)).first()
        old_ip = "127.0.0.1"
        new_ip = "192.168.1.7"
        user.avatar = replace_ip(user.avatar, old_ip, new_ip)
        return user


    async def update_user_info(self, new_user_info: UserUpdate,id,session: Depends):
        user = session.query(models.User).filter(models.User.id == id)
    
        user.update({"username" : new_user_info.username,"personal_signature" : new_user_info.personal_signature,"alias" : new_user_info.alias})
        session.commit()
        return user.first()        

    async def change_password(self,change:ChangePassword,user_id,session: Depends):
        NewPass = change.new_pass
        OldPass = change.old_password
        user = session.query(models.User).filter(models.User.id == user_id)
    
        if not hashing.Hash.verify(user.first().password, OldPass):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='incorrect password')

        NewPass = hashing.Hash.bcrypt(NewPass)
        user.update({ "password" : NewPass })
        session.commit()
        return {"detail": "successfully change"}
    

    async def create_upload_file(self, file: UploadFile,token: str,session: Depends):  
        user = await self.get_user_info(token,session)
        f = await file.read()
        # return user
        if user.avatar == "https://i.sstatic.net/l60Hf.png":
            self.supabase.storage.from_("avatar").upload(
            path=f'avatar_{user.id}', file=f, file_options={"content-type": "image/jpeg"}
            )
        else:
            self.supabase.storage.from_("avatar").remove([f'avatar_{user.id}'])
            self.supabase.storage.from_("avatar").upload(
            path=f'avatar_{user.id}', file=f, file_options={"content-type": "image/jpeg"}
            )

        url = self.supabase.storage.from_('avatar').create_signed_url(path=f'avatar_{user.id}', expires_in=30000000)["signedURL"]
        new_user = session.query(models.User).filter(models.User.id == user.id)
    
        new_user.update({"avatar" : str(url)})
        session.commit()
        old_ip = "127.0.0.1"
        new_ip = "192.168.1.7"
        url = replace_ip(url, old_ip, new_ip)
        return {"url":url,"detail": "successfully upload"}

    async def delete_user(self, id,session: Depends):
        all_knowledge = session.query(
        models.knowledge.Knowledge.id,
    ).filter(
        models.knowledge.Knowledge.user_id == id
    ).all()

        for id_k in all_knowledge:
            list_file = await file_db.get_list_file_id(id_k[0],session)
            for id_f in list_file:
                self.supabase.storage.from_("file").remove([id_f])
            
        user = session.query(models.User).filter(models.User.id == id)
        user.delete()
        session.commit()
        return {"detail": "successfully delete"}


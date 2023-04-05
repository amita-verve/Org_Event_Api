from app.models.user_model import UserModel
from app.feedback_form_processig.login_schema import UserLoginSchema
from app.feedback_form_processig.register_schema import UserRegisterSchema
from app.auth.auth_handler import signJWT
from config.database import get_db
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session, load_only
from app.auth.auth_handler import Hasher
from config.database import response
from passlib.context import CryptContext
import bcrypt


class Userservices:

    def create_user(user: UserRegisterSchema,db: Session = Depends(get_db)):

        db_user_register = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_no=user.phone_no,
            password=Hasher.get_password_hash(user.password)
            
        )
           
        db.add(db_user_register)
        db.commit()
        db.refresh(db_user_register)
        token = signJWT(db_user_register.id)
        db_user_register.__dict__['token'] = token['access_token']
        del  db_user_register.__dict__['password']

        return db_user_register
    
        

        

    def login_user(user: UserLoginSchema,db: Session = Depends(get_db)):
        db_user_login = db.query(UserModel).filter(
             UserModel.email==user.email,
            ).first()
        
        if db_user_login is None:
            return False
        token = signJWT(db_user_login.id)
        db_user_login.__dict__['token'] = token['access_token']
        del  db_user_login.__dict__['password']
        return db_user_login   
    


   
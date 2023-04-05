from app.feedback_form_processig.login_schema import UserLoginSchema
from app.feedback_form_processig.register_schema import UserRegisterSchema
from app.feedback_process.user.user_login_services import Userservices
from sqlalchemy.orm import Session, load_only
from fastapi import Depends, FastAPI, HTTPException, APIRouter, Query
from config.database import get_db, response



router = APIRouter(prefix='/api', tags=["Login"])

@router.post("/register")
def Register(org:UserRegisterSchema, db: Session = Depends(get_db)):
    user=Userservices.create_user(org,db)
    return response(True,"User Register Successfullly",user)



@router.post('/login')
def Login(user: UserLoginSchema,db: Session = Depends(get_db)):
    created_user =Userservices.login_user(user,db)
    if created_user is False:
        return response(True,"User is not valid", [])
    else:
        return response(True,"User login successfully",created_user)



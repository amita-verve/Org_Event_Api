from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserRegisterSchema(BaseModel):
    first_name:str
    last_name:str
    email: str
    phone_no:int
    password: str
 
 
    class Config:
        orm_mode = True
from passlib.context import CryptContext
import time
from typing import Dict
import jwt
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def signJWT(user_id: str) -> Dict[str, str]:

    print(jwt.__file__)

    payload = {
        "user_id": user_id,
        "expires": time.time() + 86400
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    tokenResponse = {
        "access_token": token
    }

    return tokenResponse


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

  

class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
    

   
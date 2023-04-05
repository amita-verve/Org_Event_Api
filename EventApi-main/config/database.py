from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, session
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

SQLALCHEMY_DB_URL = ("mysql+mysqlconnector://"+os.getenv("DB_USERNAME")+"@"+os.getenv("DB_HOST")+":"+os.getenv("DB_PORT")+"/"+os.getenv("DB_DATABASE"))

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DB_URL)

conn = engine.connect()

SessionLocal = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def response(status, message, data):
    return {
        "status": status,
        "message": message,
        "data": data,
    }


def configure_jwt(app):
    @AuthJWT.load_config
    def get_config():
        return AuthSettings(
            SECRET_KEY=SECRET_KEY,
            ALGORITHM="HS256",
            ACCESS_TOKEN_EXPIRE_MINUTES=30,
            REFRESH_TOKEN_EXPIRE_DAYS=30
        )

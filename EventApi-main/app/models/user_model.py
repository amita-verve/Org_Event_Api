# from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String,func,DateTime
from config.database import Base


class UserModel(Base):
        __tablename__ = 'user'

        id = Column((Integer),primary_key=True)
        first_name=Column(String(255),nullable=False)
        last_name=Column(String(255),nullable=False)
        email = Column(String(255), nullable=False,unique=True)
        phone_no=Column(String(255),nullable=False)
        password=Column(String(255),nullable=False)
        created_at = Column(DateTime, default=func.now())
        updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
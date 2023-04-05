from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date, time


class MeetupSchema(BaseModel):

    meetup_name: str
    meetup_description: Optional[str] = None
    meetup_type: Optional[str] = None
    track: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

    class Config:
        orm_mode = True

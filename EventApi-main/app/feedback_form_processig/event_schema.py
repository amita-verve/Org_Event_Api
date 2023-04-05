from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class EventSchema(BaseModel):

    event_name: str
    event_description: str
    event_type: Optional[str] = None
    event_id:int
    meetup_id:int
    topic: str
    speaker: str
    start_time: datetime
    end_time: datetime
    day: date

    class Config:
        orm_mode = True

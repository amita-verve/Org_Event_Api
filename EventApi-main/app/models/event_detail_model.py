from sqlalchemy import  Column, Integer, String, DateTime, Date
from sqlalchemy import ForeignKey
from app.models.event_model import EventModel
from sqlalchemy.orm import relationship
from config.database import Base



class EventDetail(Base):
    __tablename__ = "event_detail"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer ,ForeignKey('event.id'), index=True)
    topic = Column(String(255))
    speaker = Column(String(255), nullable=True)
    start_time = Column(DateTime,nullable=False)
    end_time = Column(DateTime,nullable=False)
    day = Column(Date,nullable=True)
    event = relationship("EventModel", back_populates="event_details")

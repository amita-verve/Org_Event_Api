from config.database import Base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.models.meetup_model import MeetupModel

class EventModel(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(150), nullable=False)
    event_description = Column(String(255), nullable=True)
    event_type = Column(Enum("webinar", "seminar", "presentation"), nullable=True)
    meetup_id = Column(Integer,ForeignKey("meetup.id"),unique=False)
    events_meetup = relationship(MeetupModel, back_populates='meetups')
    event_details = relationship("EventDetail", back_populates="event")




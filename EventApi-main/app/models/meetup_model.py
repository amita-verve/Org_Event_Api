from sqlalchemy import Column, Integer, String, Text, Enum, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base




class MeetupModel(Base):

    __tablename__ = 'meetup'

    id = Column(Integer, primary_key=True)
    meetup_name = Column(String(255), nullable=False)
    meetup_description = Column(Text)
    meetup_type = Column(Enum("webinar", "seminar", "presentation"), nullable=True)
    track = Column(Enum('single', 'multi day'),nullable=True)
    start_date = Column(Date,nullable=False)
    end_date = Column(Date,nullable=False)
    start_time = Column(Time,nullable=False)
    end_time = Column(Time,nullable=False)

    meetups = relationship('EventModel', uselist=False, back_populates='events_meetup')

   
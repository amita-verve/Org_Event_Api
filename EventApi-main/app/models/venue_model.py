from sqlalchemy import Column, Integer, String, Float
from config.database import Base

class Venue(Base):
    __tablename__ = 'venue_master'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255),nullable=True)
    city = Column(String(255),nullable=False)
    state = Column(String(255),nullable=False)
    zip = Column(String(10),nullable=True)
    landmark_01 = Column(String(255),nullable=False)
    landmark_02 = Column(String(255),nullable=True)
    geo_location_address = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

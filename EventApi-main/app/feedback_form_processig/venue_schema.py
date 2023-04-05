from pydantic import BaseModel


class VenueCreate(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip: str
    landmark_01: str
    landmark_02: str
    geo_location_address: str
    latitude: float
    longitude: float


class Config:
        orm_mode = True
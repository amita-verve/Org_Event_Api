from pydantic import BaseModel
from typing import Optional, List


class OrganisationSchema(BaseModel):
    
    name: str
    address: str
    city: str
    state: str
    zip: int
    org_type: str
    


    class Config:
        orm_mode = True

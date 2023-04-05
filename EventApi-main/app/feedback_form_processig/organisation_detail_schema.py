from pydantic import BaseModel


class OrganisationDetailSchema(BaseModel):
        org_id:int
        name:str
        email: str
        phone: str
        designation: str

        class Config:
            orm_mode = True

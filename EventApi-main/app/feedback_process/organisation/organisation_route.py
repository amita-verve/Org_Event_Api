from fastapi import Depends, FastAPI, APIRouter
from config.database import get_db
from sqlalchemy.orm import Session
from config.database import SessionLocal
from app.models.organisation_model import OrganisationModel
from app.models.organisation_contact_model import OrganizationContactModel
from app.feedback_form_processig.organisation_schema import OrganisationSchema
from app.feedback_process.organisation.organisation_services import Organisationservices
from typing import List
from config.database import get_db, response
from sqlalchemy.orm import Session
from fastapi_pagination import paginate,  Params
from fastapi import FastAPI, Depends, HTTPException
from app.auth.auth_bearer import JWTBearer

router = APIRouter(prefix="/Organisation", tags=["organisation"], dependencies=[Depends(JWTBearer())])



@router.get("/get_organizations_list/")
def get_all_org(search: str = "", params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):
    all_org = Organisationservices.get_all_org(
        search, params, sort_by, sort_direction, db)
    return response(True, "alL organization list", all_org)


@router.get("/get_organisations_by_id/{id}")
def get_organization(id: int,db: Session = Depends(get_db)):

    db_org = Organisationservices.get_organization(id, db)
    if db_org==None:
        return (True,"id is not valid",None)
    else:    
        return response(True, "organization detail ", db_org)




@router.post("/create_organisation/")
def create_org(org: OrganisationSchema, db: Session = Depends(get_db)):
    print(org)
    db_org = Organisationservices.create_organization(org, db)
    return response(True, "organisation created", db_org)


@router.put("/update_organisation/{id}")
def update_org(id: int, org: OrganisationSchema, db: Session = Depends(get_db)):
    db_org = Organisationservices.update_org(id, org, db)
    if db_org==None:
        return (True,"id is not valid",None)
    else:    
        return response(True, " organisation updated ", db_org)


@router.delete("/delete_organisation/{id}")
def delete_org(id: int, db: Session = Depends(get_db)):
    all_org = Organisationservices.delete_org(id=id, db=db)
    if all_org is None:
        return response(True, "ID does not exists  ", None)
    else:    
        return response(True, " organisation deleted ", all_org)

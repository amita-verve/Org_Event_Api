from fastapi import Depends, FastAPI, HTTPException, APIRouter, Query
from config.database import get_db
from sqlalchemy.orm import Session
from config.database import SessionLocal
from app.models.organisation_model import OrganisationModel
from app.models.organisation_contact_model import OrganizationContactModel
from app.feedback_form_processig.organisation_schema import OrganisationSchema
from app.feedback_form_processig.organisation_detail_schema import OrganisationDetailSchema
from app.feedback_process.organisationdetail.organisation_detail_services import Organisationdetailservices 
from typing import List
from config.database import get_db, response
from sqlalchemy.orm import Session
from fastapi_pagination import paginate,  Params
from app.auth.auth_bearer import JWTBearer


router = APIRouter(prefix="/Organisationdetails", tags=["OrganisationDetail"],dependencies=[Depends(JWTBearer())])

@router.get("/get_organizationdetail_list/")
def get_all_org_route(search: str = "", params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):
    all_org = Organisationdetailservices.get_all_orgdetail(
        search, params, sort_by, sort_direction, db)
    return response(True, "all organization", all_org)

@router.get("/get_organisation_by_id/{id}")
def get_organization_route(id: int, db: Session = Depends(get_db)):
    db_org = Organisationdetailservices.get_organizationdetail(id, db)
    if db_org is None:
        return response(False, "Organization not found", None)
    else:
        return response(True, "Organization found", db_org)
        

@router.post("/create_organisation/")
def create_org_route(org: OrganisationDetailSchema, db: Session = Depends(get_db)):
    print(org)
    db_org = Organisationdetailservices.create_organizationdetail(org, db)
    return response(True, "organistaiondetail created", db_org)

@router.put("/update_organisation/{id}")
def update_org_route(id: int, org: OrganisationDetailSchema, db: Session = Depends(get_db)):
    db_org = Organisationdetailservices.update_orgdetail(id,org,db)
    if not db_org:
        return ("id is not valid")
    else:
        return response(True, "  organisationdetail  updated ", db_org)

@router.delete("/delete_organisation/{id}")
def delete_org_route(id: int, db: Session = Depends(get_db)):
    all_org = Organisationdetailservices.delete_orgdetail(id=id, db=db)
    if not all_org:
        return(True,"id is not valid",None)
    return response(True, "organisationdetail delete", all_org)







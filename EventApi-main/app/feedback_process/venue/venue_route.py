from fastapi import FastAPI,  Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from app.feedback_form_processig.venue_schema import VenueCreate
from app.feedback_process.venue.venue_services import VenueServices
from config.database import get_db, response
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Page, Params
from app.models.venue_model import Venue
from app.feedback_form_processig.venue_schema import VenueCreate
from app.auth.auth_bearer import JWTBearer


router = APIRouter(prefix="/venue", tags=["venue"],dependencies=[Depends(JWTBearer())])

@router.get("/get_venuelist/")
def get_all_venue(search: str = "", params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):
    all_venue = VenueServices.get_all_venue(search, params, sort_by, sort_direction, db)
    return response(True, "all  venue", all_venue)

@router.get("/get_venue/{venue_id}")
def get__venue(venue_id: int, db: Session = Depends(get_db)):
    db_venue = VenueServices.get_venue(venue_id, db)
    if db_venue == None:
        return response(True, "Venue not found !",None)
    return response(True, "venue found !", db_venue)


@router.post("/create_venue/")
def create_venue(org: VenueCreate, db: Session = Depends(get_db)):
    print(org)
    db_venue = VenueServices.create_venue(org, db)
    return response(True, "venue created", db_venue)


@router.put("/update_venue/{venue_id}")
def update_venue(venue_id: int, org: VenueCreate, db: Session = Depends(get_db)):
    db_venue = VenueServices.update_venue(venue_id, org, db)
    if not db_venue:
        return ("id is not valid")
    else:
        return response(True, "venue updated", db_venue)


@router.delete("/delete_venue/{venue_id}")
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    all_venue =VenueServices. delete_venue(org_id=venue_id, db=db)
    return response(True, "deleted", all_venue)

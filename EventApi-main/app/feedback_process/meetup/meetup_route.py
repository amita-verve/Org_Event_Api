from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from app.models.meetup_model import MeetupModel
from app.feedback_form_processig.meetup_schema import MeetupSchema
from app.feedback_process.meetup.meetup_services import MeetupServices
from config.database import get_db, response
from sqlalchemy.orm import Session, load_only
from fastapi_pagination import paginate, Page, Params
from sqlalchemy import desc, asc, or_
from app.auth.auth_bearer import JWTBearer


router = APIRouter(prefix="/meetup", tags=["meetup"],dependencies=[Depends(JWTBearer())])

@router.get("/get_meetup_list/")
def get_all_meetup(search: str = "", params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):
    all_meetup = MeetupServices.get_all_meetup(
        search, params, sort_by, sort_direction, db)
    return response(True, "all meetup list ", all_meetup)

@router.get("/get_meetup_by_id/{id}")
def get_meetup(id: int, db: Session = Depends(get_db)):
    db_meetup = MeetupServices.get_meetup(id, db)
    if not db_meetup:
        return ("id is not valid")
    else:
        return response(True, "meetup found ", db_meetup)


@router.post("/create_meetup/")
def create_meetup(org: MeetupSchema, db: Session = Depends(get_db)):
    print(org)
    db_meetup = MeetupServices.create_meetup(org, db)
    return response(True, "meetup created", db_meetup)

@router.put("/update_meetup/{id}")
def update_meetup(id: int, org: MeetupSchema, db: Session = Depends(get_db)):
    db_meetup = MeetupServices.update_meetup(id, org, db)
    if not db_meetup:
        return ("id is not valid")
    else:
        return response(True, "meetup updated ", db_meetup)


@router.delete("/delete_meetup/{id}")
def delete_meetup(id: int, db: Session = Depends(get_db)):
    all_meetup = MeetupServices.delete_meetup(id=id, db=db)
    return response(True, "meetup deleted", all_meetup)






from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from app.feedback_form_processig.event_schema import EventSchema
from config.database import get_db, response
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Page, Params
from app.feedback_process.event.event_services import EventService
from app.models.event_model import EventModel
from app.models.event_detail_model import EventDetail
from app.auth.auth_bearer import JWTBearer


router = APIRouter(prefix="/Event", tags=["Event"],dependencies=[Depends(JWTBearer())])


@router.get("/get_eventlist/")
def get_all_event(db: Session = Depends(get_db)):
    all_event = EventService.get_all_event(db)
    return response(True, "all event list", all_event)


@router.get('/get_event_by_id/{id}', summary="Get event by ID")
def getEvent(id: int, db: Session = Depends(get_db)):
    event = EventService.get_event(id=id, db=db)
    if event == None:
        return response(True, "Event id  not found !", None)
    return response(True, "Event found !", event)


@router.post("/create_event/")
def create_event(org: EventSchema, db: Session = Depends(get_db)):
    db_event = EventService.create_event(org, db)
    return response(True, "event created", db_event)


@router.put("/update_event/{id}")
def update_event(id: int, org: EventSchema, db: Session = Depends(get_db)):
    db_event = EventService.update_event(id, org, db)
    return response(True, "event updated  ", db_event)


@router.delete("/delete_event/{id}")
def delete_event(id: int, db: Session = Depends(get_db)):
    all_event = EventService.delete_event(id=id, db=db)
    if all_event:
        return response(True, " event deleted", all_event)





from sqlalchemy.orm import Session
from config.database import SessionLocal, get_db
from app.models.event_detail_model import EventDetail
from app.feedback_form_processig.event_schema import EventSchema
from fastapi import Depends
from sqlalchemy.orm import Session, load_only
from app.models.event_model import EventModel
from app.models.event_detail_model import EventDetail
from config.database import get_db
from typing import List
from sqlalchemy.orm import Session, load_only,joinedload

class EventService:

    def get_event(id: int, db: Session = Depends(get_db)):
        event_model=db.query(EventModel).filter(EventModel.id==id).first()
        event = db.query(EventDetail).filter(EventDetail.event_id == id).first()
        return event,event_model


    def create_event(org: EventSchema, db: Session = Depends(get_db)):
        db_event = EventModel(event_name=org.event_name, meetup_id=org.meetup_id, event_description=org.event_description,
                            event_type=org.event_type)
        db.add(db_event)
        db.commit()
        
        events = EventDetail(topic=org.topic, speaker=org.speaker, event_id=db_event.id,
                        start_time=org.start_time, end_time=org.end_time,day=org.day)
        db.add(events)
        db.commit()
        db.refresh(events)

        return {
            "event_model": db_event,
            "event_detail": events
        }


    def get_all_event(db: Session = Depends(get_db)):  # ,params: Params = Depends(),
        query = db.query(EventModel).options(joinedload(EventModel.event_details))
        events = query.all()
        return events

        
    def update_event(event_id: int, org: EventSchema, db: Session = Depends(get_db)):
        db_event = db.query(EventDetail).filter(
            EventDetail.id == event_id).first()
        if db_event is None:
            return None
        for attr, value in vars(org).items():
            setattr(db_event, attr, value) if value else None
        db.commit()
        db.refresh(db_event)
        return db_event



    def delete_event(id: int, db: Session = Depends(get_db)):
        db_event = db.query(EventDetail).filter(EventDetail.id == id).first()
        if not db_event:
            return (True,"Event detail not found",None)
        db.delete(db_event)
        db.commit()
        return {"message": "Event deleted successfully"}    


  


  
    

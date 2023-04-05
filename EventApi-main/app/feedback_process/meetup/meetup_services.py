from sqlalchemy.orm import Session
from config.database import SessionLocal, get_db
from app.models.meetup_model import MeetupModel
from app.models.event_model import EventModel
from app.models.event_detail_model import EventDetail
from fastapi import Depends, HTTPException
from fastapi_pagination import paginate, Page, Params
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session, load_only
from app.feedback_form_processig.meetup_schema import MeetupSchema
from config.database import get_db, response
from datetime import date, timedelta
from sqlalchemy import text

class MeetupServices:

    def get_meetup(id: int, db: Session = Depends(get_db)):
        db_meetup = db.query(MeetupModel).filter(
            MeetupModel.id == id).first()

        return db_meetup

    def create_meetup(org: MeetupSchema, db: Session = Depends(get_db)):
        db_meetup = MeetupModel(meetup_name=org.meetup_name, meetup_description=org.meetup_description, meetup_type=org.meetup_type,
                                track=org.track, start_date=org.start_date, end_date=org.end_date, start_time=org.start_time, end_time=org.end_time)
        db.add(db_meetup)
        db.commit()
        db.refresh(db_meetup)
        return db_meetup

    def update_meetup(id: int, org: MeetupSchema,  db: Session = Depends(get_db)):
        db_meetup = db.query(MeetupModel).filter(
            MeetupModel.id == id).first()
        if db_meetup is None:
            return None
        for attr, value in vars(org).items():
             setattr(db_meetup, attr, value) if value else None
        db.add(db_meetup)     
        db.commit()
        db.refresh(db_meetup)
        return db_meetup



    
    def get_all_meetup(search: str, params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):  # ,params: Params = Depends(),
        fetch_org = db.query(MeetupModel).options(
            load_only(MeetupModel.id, MeetupModel.meetup_name,MeetupModel.meetup_type,MeetupModel.start_date,MeetupModel.end_date,MeetupModel.start_time,MeetupModel.end_time,MeetupModel.meetup_description,MeetupModel.track))
        print(fetch_org)
        if sort_direction == "desc":
            fetch_org = fetch_org.order_by(
                MeetupModel.__dict__[sort_by].desc())
        elif sort_direction == "asc":
            fetch_org = fetch_org.order_by(
                MeetupModel.__dict__[sort_by].asc())
        else:
            fetch_org = fetch_org.order_by(MeetupModel.id.desc())

        updated_all_org = fetch_org.all()
        if search:
            fetch_org = fetch_org.filter(or_(
                MeetupModel.meetup_name.like('%'+search+'%'),
            ))
            return response(True, " get all meetup ", updated_all_org)

        return paginate(updated_all_org, params)


 
    def delete_meetup(id: int, db: Session):
        db_org = db.query(MeetupModel).filter(
        MeetupModel.id == id).first()
        if db_org is not None:
            events=db.query(EventModel).filter(EventModel.meetup_id==id).all()
            print(type(events))
            for event in events:
                event_details=db.query(EventDetail).filter(EventDetail.event_id==event.id).delete()
                print(event_details)
                db.commit()
                db.delete(event)
                db.commit()
                
        db.delete(db_org)
        db.commit()
        return True

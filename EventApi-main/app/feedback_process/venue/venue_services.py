from sqlalchemy.orm import Session
from config.database import SessionLocal, get_db
from app.models.venue_model import Venue
from app.feedback_form_processig.venue_schema import VenueCreate
from fastapi import Depends, HTTPException
from fastapi_pagination import paginate, Page, Params
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session, load_only
from config.database import get_db, response

class VenueServices:
    def get_venue(org_id: int, db: Session = SessionLocal()):
        db_venue = db.query(Venue).filter(
            Venue.id == org_id).first()
        return db_venue



    def create_venue(org: VenueCreate, db: Session):
        db_venue = Venue (name=org.name, address=org.address,city=org.city,state=org.state,zip=org.zip,landmark_01=org.landmark_01,landmark_02=org.landmark_02,
                                geo_location_address=org.geo_location_address,latitude=org.latitude,longitude=org.longitude)
        db.add(db_venue)
        db.commit()
        db.refresh(db_venue)
        return db_venue


    def update_venue(org_id: int, org: VenueCreate, db: Session = SessionLocal()):
        db_venue = db.query(Venue).filter(
            Venue.id == org_id).first()
        if db_venue is None:
            return None
        for attr, value in vars(org).items():
            setattr(db_venue, attr, value) if value else None
        db.commit()
        db.refresh(db_venue)
        return db_venue


    def delete_venue(org_id: int, db: Session):
        db_venue = db.query(Venue).filter(
            Venue.id == org_id).first()
        if db_venue is None:
            return None
        db.delete(db_venue)
        db.commit()
        return db_venue





    def get_all_venue(search: str, params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):  # ,params: Params = Depends(),
        fetch_org = db.query(Venue).options(
            load_only(Venue.id, Venue.name,Venue.address,Venue.city,Venue.geo_location_address,Venue.landmark_01,Venue.landmark_02,Venue.latitude,Venue.longitude))
        print(fetch_org)
        if sort_direction == "desc":
            fetch_org = fetch_org.order_by(
                Venue.__dict__[sort_by].desc())
        elif sort_direction == "asc":
            fetch_org = fetch_org.order_by(
                Venue.__dict__[sort_by].asc())
        else:
            fetch_org = fetch_org.order_by(Venue.id.desc())

        updated_all_org = fetch_org.all()
        if search:
            fetch_org = fetch_org.filter(or_(
                Venue.name.like('%'+search+'%'),
                Venue.address.like('%'+search+'%'),
            ))
            return response(True, " get all organisation ", updated_all_org)

        return paginate(updated_all_org, params)


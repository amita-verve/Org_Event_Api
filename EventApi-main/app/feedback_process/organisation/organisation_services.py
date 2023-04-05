from sqlalchemy.orm import Session
from config.database import SessionLocal, get_db
from app.models.organisation_model import OrganisationModel
from app.models.organisation_contact_model import OrganizationContactModel
from app.feedback_form_processig.organisation_schema import OrganisationSchema
from fastapi import Depends
from fastapi_pagination import paginate, Page, Params
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session, load_only
from config.database import get_db, response
from typing import List


class Organisationservices:

    def get_organization(org_id: int, db: Session = SessionLocal()):
        result = db.query(OrganisationModel).outerjoin(
            OrganizationContactModel).filter(OrganisationModel.id ==org_id).first()
        return result
    
    
 

    def update_organization(org_id: int, org: OrganisationSchema, db: Session = SessionLocal()):
        db_org = db.query(OrganisationModel).filter(
            OrganisationModel.id == org_id).first()

        if db_org is None:
            return None
        for attr, value in vars(org).items():
            setattr(db_org, attr, value) if value else None

        db.commit()
        db.refresh(db_org)
        return db_org

    def get_all_org(search: str, params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):  # ,params: Params = Depends(),
        fetch_org = db.query(OrganisationModel).options(
            load_only(OrganisationModel.id, OrganisationModel.name,OrganisationModel.address,OrganisationModel.city,OrganisationModel.org_type,OrganisationModel.state,OrganisationModel.zip))
        print(fetch_org)
        if sort_direction == "desc":
            fetch_org = fetch_org.order_by(
                OrganisationModel.__dict__[sort_by].desc())
        elif sort_direction == "asc":
            fetch_org = fetch_org.order_by(
                OrganisationModel.__dict__[sort_by].asc())
        else:
            fetch_org = fetch_org.order_by(OrganisationModel.id.desc())

        updated_all_org = fetch_org.all()
        if search:
            fetch_org = fetch_org.filter(or_(
                OrganisationModel.name.like('%'+search+'%'),
            ))

        return paginate(updated_all_org, params)

    def create_organization(org: OrganisationSchema, db: Session):
        db_org = OrganisationModel(name=org.name, address=org.address,
                                   city=org.city,
                                   state=org.state,
                                   zip=org.zip,
                                   org_type=org.org_type,
                                   )

      
       
       

        db.add(db_org)
        db.flush()
        db.commit()
        db.refresh(db_org)
        return db_org

    def update_org(id: int, org: OrganisationSchema,  db: Session = Depends(get_db)):
        db_meetup = db.query(OrganisationModel).filter(
            OrganisationModel.id == id).first()
        if db_meetup is None:
            return None
        for attr, value in vars(org).items():
            setattr(db_meetup, attr, value) if value else None
        db.commit()
        db.refresh(db_meetup)
        return db_meetup
    
    def delete_org(id: int, db: Session = Depends(get_db)):
        with db:
            db_org = db.query(OrganisationModel).filter(OrganisationModel.id == id).first()
            if db_org is None:
                return None
            db.delete(db_org)
            db.commit()
            return db_org

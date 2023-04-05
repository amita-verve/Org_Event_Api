from sqlalchemy.orm import Session
from config.database import SessionLocal, get_db
from app.models.organisation_model import OrganisationModel
from app.models.organisation_contact_model import OrganizationContactModel
from app.feedback_form_processig.organisation_detail_schema import OrganisationDetailSchema
from fastapi import Depends
from fastapi_pagination import paginate, Page, Params
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session, load_only
from config.database import get_db, response
from typing import List


class Organisationdetailservices:

    def get_organizationdetail(org_id: int, db: Session = Depends(get_db)):
        result = db.query(OrganizationContactModel).filter(OrganizationContactModel.id ==org_id).first()
        return result


    def update_organizationdetail(org_id: int, org: OrganisationDetailSchema, db: Session = SessionLocal()):
        db_org = db.query(OrganizationContactModel).filter(
            OrganizationContactModel.id == org_id).first()

        if db_org is None:
            return None
        for attr, value in vars(org).items():
            setattr(db_org, attr, value) if value else None

        db.commit()
        db.refresh(db_org)
        return db_org

    def get_all_orgdetail(search: str, params: Params = Depends(), sort_by: str = None, sort_direction: str = None, db: Session = Depends(get_db)):  # ,params: Params = Depends(),
        fetch_org = db.query(OrganizationContactModel).options(
            load_only(OrganizationContactModel.org_id,OrganizationContactModel.designation,OrganizationContactModel.phone,OrganizationContactModel.name,OrganizationContactModel.email))
        if sort_direction == "desc":
            fetch_org = fetch_org.order_by(
                OrganizationContactModel.__dict__[sort_by].desc())
        elif sort_direction == "asc":
            fetch_org = fetch_org.order_by(
                OrganizationContactModel.__dict__[sort_by].asc())
        else:
            fetch_org = fetch_org.order_by(OrganizationContactModel.id.desc())

        updated_all_org = fetch_org.all()
        if search:
            fetch_org = fetch_org.filter(or_(
                OrganizationContactModel.name.like('%'+search+'%'),
            ))

        return paginate(updated_all_org, params)

    def delete_orgdetail(id: int, db: Session):
        db_org = db.query(OrganizationContactModel).filter(
            OrganizationContactModel.id == id).first()
        db_orgs = db.query(OrganizationContactModel).filter(
            OrganizationContactModel.id == id).all()
        if db_org is None:
            return None
        db.delete(db_org)
        for org_contact in db_orgs:
            db.delete(org_contact)
        db.commit()
        return db_org

    def create_organizationdetail(org: OrganisationDetailSchema, db: Session):

        db_org_contact = OrganizationContactModel(org_id=org.org_id,
             email=org.email,name=org.name, phone=org.phone, designation=org.designation)
        db.add(db_org_contact)
        print(db_org_contact)
        db.commit()
        db.refresh(db_org_contact)
        return db_org_contact

    def update_orgdetail(id: int, org: OrganisationDetailSchema,  db: Session ):
        db_meetup = db.query(OrganizationContactModel).filter(
            OrganizationContactModel.id == id).first()
        if db_meetup is None:
            return None
        for attr, value in vars(org).items():
            setattr(db_meetup, attr, value) if value else None
        db.commit()
        db.refresh(db_meetup)
        return db_meetup

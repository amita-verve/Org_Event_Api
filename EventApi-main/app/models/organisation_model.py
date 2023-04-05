from config.database import Base
from sqlalchemy import String, Integer, Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.models.organisation_contact_model import OrganizationContactModel


class OrganisationModel(Base):
     
     __tablename__ = "organisation"
     id = Column(Integer,primary_key=True,index=True,nullable=False)
     name = Column(String(50), nullable=False)
     address=Column(String(50),nullable=True)
     city = Column(String(255), nullable=True)
     state=Column(String(255), nullable=True)
     zip=Column(Integer, nullable=True)
     org_type=Column(String(255), nullable=True)
     contacts = relationship(OrganizationContactModel, back_populates='org')






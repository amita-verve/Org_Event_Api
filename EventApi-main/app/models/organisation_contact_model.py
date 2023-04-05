from config.database import Base
from sqlalchemy import String, Integer, Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class OrganizationContactModel(Base):
      __tablename__ = "organization_contacts"
      id = Column(Integer, primary_key=True, index=True)
      org_id = Column(Integer,ForeignKey("organisation.id"),unique=False,nullable=False)
      name = Column(String(255), nullable=False)
      email = Column(String(255),nullable=True)
      phone = Column(String(20),nullable=False)
      designation = Column(String(255),nullable=True)
      
      org = relationship('OrganisationModel', uselist=False, back_populates='contacts')

    
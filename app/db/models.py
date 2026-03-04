from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    org_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="users")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    org_id = Column(Integer, ForeignKey("organizations.id"))
    uploaded_by = Column(Integer, ForeignKey("users.id"))

    organization = relationship("Organization")
    user = relationship("User")
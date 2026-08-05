from sqlalchemy import Column, Integer, String, Boolean, Enum, func
from ..db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from enum import Enum as PyEnum


class Role(PyEnum):
    admin = "admin"
    member = "member"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(Role),nullable=False, server_default=Role.member.value)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    projects = relationship("Project", back_populates="owner")


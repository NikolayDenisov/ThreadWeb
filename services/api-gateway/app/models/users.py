from sqlalchemy import Boolean, Column, Integer, String, DateTime, text, ForeignKey
from sqlalchemy import event, DDL
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    description = Column(String(160))
    is_active = Column(Boolean, default=True)


class Token(Base):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    token = Column(UUID(as_uuid=False), server_default=text("uuid_generate_v4()"), unique=True, nullable=False,
                   index=True)
    expires = Column(DateTime())
    user_id = Column(Integer, ForeignKey("user.id"))

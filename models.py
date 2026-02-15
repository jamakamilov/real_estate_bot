import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, BigInteger, String,
    Boolean, DateTime, Enum, ForeignKey
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserRole(str, enum.Enum):
    user = "user"
    private = "private"
    agent = "agent"
    admin = "admin"

class ListingStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    role = Column(Enum(UserRole), default=UserRole.user)
    is_pro = Column(Boolean, default=False)
    pro_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    owner_id = Column(BigInteger, ForeignKey("users.id"))
    title = Column(String)
    price = Column(Integer)
    city = Column(String)

    status = Column(Enum(ListingStatus), default=ListingStatus.pending)

    views = Column(Integer, default=0)

    is_boosted = Column(Boolean, default=False)
    boosted_until = Column(DateTime, nullable=True)

    expires_at = Column(DateTime)
    is_archived = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

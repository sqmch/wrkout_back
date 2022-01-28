from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from wrkout2_back.database import Base


class User(Base):
    """User sqlalchemy model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    routines = relationship("Routine", back_populates="owner")


class Routine(Base):
    """Workout routine sqlalchemy model"""

    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="routines")
    exercises = Column(String, index=True)

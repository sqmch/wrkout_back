from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from wrkout2_back.database import Base


class User(Base):
    """User sqlalchemy model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    routines = relationship("Routine", back_populates="owner")


class Routine(Base):
    """Workout routine sqlalchemy model"""

    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    exercises = relationship("Exercise", back_populates="owner")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="routines")


class Exercise(Base):
    """Exercise sqlalchemy model"""

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    rest_time = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("routines.id"))
    owner = relationship("Routine", back_populates="exercises")

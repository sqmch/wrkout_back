from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from wrkout2_back.database import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    routines = relationship("Routine", back_populates="owner")
    performed_routines = relationship("PerformedRoutine", back_populates="owner")


class Routine(Base):
    """Workout routine model"""

    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    exercises = relationship("Exercise", back_populates="owner")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="routines")


class Exercise(Base):
    """Exercise model"""

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    rest_time = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("routines.id"))
    owner = relationship("Routine", back_populates="exercises")


class PerformedRoutine(Base):
    """Performed workout routine model"""

    __tablename__ = "performed_routines"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    performed_exercises = relationship("PerformedExercise", back_populates="owner")
    owner = relationship("User", back_populates="performed_routines")


class PerformedExercise(Base):
    """Performed exercise model"""

    __tablename__ = "performed_exercises"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    reps = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("performed_routines.id"))
    owner = relationship("PerformedRoutine", back_populates="performed_exercises")

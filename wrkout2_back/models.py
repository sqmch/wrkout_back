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


"""
      op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("routines", sa.String),
    )

    op.create_table(
        "routines",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.Column("owner", sa.String),
        sa.Column("exercises", sa.String),
    )
    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("rest_time", sa.Integer),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.Column("owner", sa.String),
    )

"""

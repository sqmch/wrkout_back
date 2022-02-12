from typing import List, Optional
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    """Base pydantic model for exercise models"""

    title: str
    description: Optional[str] = None
    rest_time: Optional[int] = 90


class ExerciseCreate(ExerciseBase):
    """Base pydantic model for exercise creation"""


class Exercise(ExerciseBase):
    """Pydantic model for an exercise"""

    id: int
    owner_id: int

    class Config:
        """Config class for Routine"""

        orm_mode = True


class RoutineBase(BaseModel):
    """Base pydantic model for workout routine models"""

    title: str
    description: Optional[str] = None
    exercises: Optional[List[Exercise]] = []


class RoutineCreate(RoutineBase):
    """Base pydantic model for workout routine creation"""


class Routine(RoutineBase):
    """Pydantic model for a workout routine"""

    id: int
    owner_id: int

    class Config:
        """Config class for Routine"""

        orm_mode = True


class UserBase(BaseModel):
    """Base pydantic class for User models"""

    username: str


class UserCreate(UserBase):
    """Base pydantic model for user creation"""

    password: str


class User(UserBase):
    """Pydantic model for a user"""

    id: int
    hashed_password: str
    is_active: bool
    routines: List[Routine]

    class Config:
        """Config class for User"""

        orm_mode = True

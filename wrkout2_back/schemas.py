from pydoc import describe
from typing import List, Optional

from pydantic import BaseModel


class AuthDetails(BaseModel):
    """Base pydantic model for authorization credentials"""

    username: str
    password: str


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
    exercises: List[Exercise]


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

    email: str


class UserCreate(UserBase):
    """Base pydantic model for user creation"""

    password: str


class User(UserBase):
    """Pydantic model for a user"""

    id: int
    is_active: bool
    routines: List[Routine]

    class Config:
        """Config class for User"""

        orm_mode = True

from typing import List, Optional

from pydantic import BaseModel


class RoutineBase(BaseModel):
    """Base pydantic model for workout routine models"""

    title: str
    description: Optional[str] = None
    exercises: str


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
    routines: List

    class Config:
        """Config class for User"""

        orm_mode = True

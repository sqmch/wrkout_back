from sqlalchemy.orm import Session
from wrkout2_back import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_routines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Routine).offset(skip).limit(limit).all()


def create_user_routine(db: Session, routine: schemas.RoutineCreate, user_id: int):
    db_routine = models.Routine(**routine.dict(), owner_id=user_id)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db_routine


def create_exercise(db: Session, exercise: schemas.ExerciseCreate, routine_id: int):
    """Add new exercise to db"""
    db_exercise = models.Exercise(**exercise.dict(), owner_id=routine_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def get_exercises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Exercise).offset(skip).limit(limit).all()

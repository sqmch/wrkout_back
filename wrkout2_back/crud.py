from sqlalchemy.orm import Session
from sqlalchemy import and_
from wrkout2_back import models, schemas
from wrkout2_back.auth import AuthHandler


auth_handler = AuthHandler()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Creates user in DB"""
    # fake_hashed_password = user.password + "notreallyhashed"
    hashed_password = auth_handler.get_password_hash(user.password)

    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_routines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Routine).offset(skip).limit(limit).all()


def get_user_routines(db: Session, user_id: int):
    return db.query(models.Routine).filter(models.Routine.owner_id == user_id).all()


def get_exercises(db: Session, routine_id: int, skip: int = 0, limit: int = 100):
    # return db.query(models.Exercise).offset(skip).limit(limit).all()
    return (
        db.query(models.Exercise).filter(models.Exercise.owner_id == routine_id).all()
    )


def create_user_routine(db: Session, routine: schemas.RoutineCreate, user_id: int):
    db_routine = models.Routine(**routine.dict(), owner_id=user_id)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db_routine


def update_routine(db: Session, routine: schemas.Routine, user_id: int, id: int):
    """Edit routine details in db"""
    # db_exercise = models.Exercise(**exercise.dict(), owner_id=routine_id)
    db_routine = db.query(models.Routine).filter_by(id=id, owner_id=user_id)
    db_routine.update(routine.dict(), synchronize_session=False)
    db.commit()
    db_routine = schemas.Routine(**routine.dict(), owner_id=user_id, id=id)

    return db_routine


def update_exercise(db: Session, exercise: schemas.Exercise, routine_id: int, id: int):
    """Edit exercise details in db"""
    # db_exercise = models.Exercise(**exercise.dict(), owner_id=routine_id)

    db_exercise = db.query(models.Exercise).filter_by(id=id, owner_id=routine_id)
    db_exercise.update(exercise.dict(), synchronize_session=False)
    db.commit()
    db_exercise = schemas.Exercise(**exercise.dict(), owner_id=routine_id, id=id)
    return db_exercise


def delete_user_routine(db: Session, routine_id: int, owner_id: int):
    """Deletes routine with user id from the db"""
    db.query(models.Exercise).filter(models.Exercise.owner_id == routine_id).delete()
    db.query(models.Routine).filter_by(id=routine_id, owner_id=owner_id).delete()
    db.commit()


def create_exercise(db: Session, exercise: schemas.ExerciseCreate, routine_id: int):
    """Add new exercise to db"""
    db_exercise = models.Exercise(**exercise.dict(), owner_id=routine_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


def delete_exercise(db: Session, exercise_id: int, owner_id: int):
    """Deletes exercise from the db given the exercise id and owner routine id"""
    db.query(models.Exercise).filter_by(id=exercise_id, owner_id=owner_id).delete()
    db.commit()


# Performed routines/exercises


def create_performed_routine(
    db: Session, routine: schemas.PerformedRoutineCreate, user_id: int
):
    db_routine = models.PerformedRoutine(**routine.dict(), owner_id=user_id)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db_routine


def create_performed_exercise(
    db: Session, exercise: schemas.PerformedExerciseCreate, routine_id: int
):
    """Add new exercise to db"""
    db_exercise = models.PerformedExercise(**exercise.dict(), owner_id=routine_id)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


"""
def get_performed_routines(db: Session, user_id: int):
    return db.query(models.Routine).filter(models.Routine.owner_id == user_id).all()"""

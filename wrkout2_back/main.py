from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from wrkout2_back import crud, models, schemas
from wrkout2_back.database import SessionLocal, engine
from wrkout2_back.auth import AuthHandler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

auth_handler = AuthHandler()
users = []

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://wrkout1.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    """Generates a db instance for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", status_code=201, response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """User registration endpoint"""

    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username is taken")
    crud.create_user(db=db, user=user)

    return


@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """User login endpoint"""

    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    if not auth_handler.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user.username)

    return {"token": token, "user_id": db_user.id}


@app.get("/unprotected")
def unprotected() -> dict:
    """Test endpoint for unprotected endpoints"""
    return {"hello": "world"}


@app.get("/protected")
def protected(username=Depends(auth_handler.auth_wrapper)):
    """Test endpoint for protected endpoints"""
    return {"name": username}


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{user_id}/routines", response_model=List[schemas.Routine])
def read_user_routines(
    user_id: int,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    db_user_routines = crud.get_user_routines(db, user_id=user_id)
    if db_user_routines is None:
        raise HTTPException(status_code=404, detail="Routines not found")
    return db_user_routines


@app.post("/users/{user_id}/routines", response_model=schemas.Routine)
def create_user_routine(
    user_id: int,
    routine: schemas.RoutineCreate,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    return crud.create_user_routine(db=db, routine=routine, user_id=user_id)


@app.put(
    "/users/{user_id}/routines/{routine_id}",
    response_model=schemas.RoutineCreate,
)
def update_routine(
    user_id: int,
    routine_id: int,
    routine: schemas.RoutineCreate,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    """Endpoint for editing a workout routine"""
    return crud.update_routine(db=db, routine=routine, user_id=user_id, id=routine_id)


@app.put(
    "/users/{user_id}/routines/{routine_id}/exercises/{exercise_id}",
    response_model=schemas.ExerciseCreate,
)
def update_exercise(
    routine_id: int,
    exercise_id: int,
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    """Endpoint for editing an exercise of a workout routine"""
    return crud.update_exercise(
        db=db, exercise=exercise, routine_id=routine_id, id=exercise_id
    )


@app.delete("/users/{user_id}/routines/{routine_id}")
def delete_user_routine(
    routine_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    """Endpoint for deleting user specific workout routines"""

    crud.delete_user_routine(db=db, routine_id=routine_id, owner_id=user_id)


@app.get("/routines/", response_model=List[schemas.Routine])
def read_routine(
    username=Depends(auth_handler.auth_wrapper),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    routines = crud.get_routines(db, skip=skip, limit=limit)
    return routines


@app.post(
    "/users/{user_id}/routines/{routine_id}/exercises/", response_model=schemas.Exercise
)
def create_exercise(
    routine_id: int,
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    return crud.create_exercise(db=db, exercise=exercise, routine_id=routine_id)


@app.delete("/users/{user_id}/routines/{routine_id}/exercises/{exercise_id}")
def delete_user_routine_exercise(
    routine_id: int,
    exercise_id: int,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    """Endpoint for deleting user specific workout routines"""

    crud.delete_exercise(db=db, exercise_id=exercise_id, owner_id=routine_id)


@app.get(
    "/users/{user_id}/routines/{routine_id}/exercises/",
    response_model=List[schemas.Exercise],
)
def read_exercises(
    routine_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    exercises = crud.get_exercises(db, routine_id=routine_id, skip=skip, limit=limit)
    return exercises


@app.post(
    "/users/{user_id}/performed_routines", response_model=schemas.PerformedRoutine
)
def create_performed_routine(
    user_id: int,
    routine: schemas.PerformedRoutineCreate,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    return crud.create_performed_routine(db=db, routine=routine, user_id=user_id)


@app.post(
    "/users/{user_id}/performed_routines/{routine_id}/performed_exercises/",
    response_model=schemas.PerformedExercise,
)
def create_performed_exercise(
    routine_id: int,
    exercise: schemas.PerformedExerciseCreate,
    db: Session = Depends(get_db),
    username=Depends(auth_handler.auth_wrapper),
):
    return crud.create_performed_exercise(
        db=db, exercise=exercise, routine_id=routine_id
    )

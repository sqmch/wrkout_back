from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from wrkout2_back import crud, models, schemas
from wrkout2_back.database import SessionLocal, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


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


@app.post("/users/{user_id}/routines/", response_model=schemas.Routine)
def create_routine_for_user(
    user_id: int, routine: schemas.RoutineCreate, db: Session = Depends(get_db)
):
    return crud.create_user_routine(db=db, routine=routine, user_id=user_id)


@app.get("/routines/", response_model=List[schemas.Routine])
def read_routine(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    routines = crud.get_routines(db, skip=skip, limit=limit)
    return routines


@app.post("/routines/{routine_id}/exercises/", response_model=schemas.Exercise)
def create_exercise(
    routine_id: int, exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)
):
    return crud.create_exercise(db=db, exercise=exercise, routine_id=routine_id)


@app.get("/exercises/", response_model=List[schemas.Exercise])
def read_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exercises = crud.get_exercises(db, skip=skip, limit=limit)
    return exercises

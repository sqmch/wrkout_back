import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
try:
    SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL").replace(
        "postgres://", "postgresql://", 1
    )
except AttributeError:
    print(
        "Environment variable for DATABASE_URL not found, switching to development db"
    )
    SQLALCHEMY_DATABASE_URL = "postgresql://qweqwe:qweqwe@localhost:5432/wrkoutdb"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

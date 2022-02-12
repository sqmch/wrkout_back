from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgres://vcexmvkdgoscpm:51c848f37ab1e93745216e1e0434edb872acad6ab9e2b93adb78f691e19ad355@ec2-54-195-76-73.eu-west-1.compute.amazonaws.com:5432/d11koj45j9fsk9"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

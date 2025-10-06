from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")

engine = create_engine(URL_DATABASE, echo=True)  # echo=True shows SQL commands
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

Session = (
    sessionmaker()
)  # created a session which is a class that helps create sessions for crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

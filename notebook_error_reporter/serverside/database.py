# this is a dumpster file.
# copypaste from tutorial.
# change to pyramid style:
# https://github.com/matteoferla/MichelaNGLo-app/blob/master/michelanglo_app/models/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./error.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

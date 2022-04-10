from typing import *

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

from fastapi import FastAPI, Request


def add_create_routes(app: FastAPI, colab_only:bool=True):
    @app.post("/usages/", response_model=schemas.Usage)
    def create_usage(usage: schemas.UsageCreate, request: Request, db: Session = Depends(get_db)):
        # ip is not expected to be unique while uuid collisions are a quadrillion to one.
        if colab_only and '142.250.' not in request.client.host and '142.250.' not in request.client.host:
            raise HTTPException(403, 'Colab error reporting only.')
        return crud.create_usage(db=db, usage=usage, ip=request.client.host)

    @app.post("/errors/{uuid}/", response_model=schemas.Error)
    def create_error(uuid: str,
                     error: schemas.ErrorCreate,
                     request: Request,
                     db: Session = Depends(get_db)):
        if colab_only and '142.250.' not in request.client.host and '142.250.' not in request.client.host:
            raise HTTPException(403, 'Colab error reporting only.')
        return crud.create_error(db=db, error=error, usage_uuid=uuid, ip=request.client.host)

def add_read_one_routes(app: FastAPI):
    @app.get("/usages/{uuid}", response_model=schemas.Usage)
    def read_usage(uuid: str, db: Session = Depends(get_db)):
        db_usage = crud.get_usage(uuid, db=db)
        if db_usage is None:
            raise HTTPException(status_code=404, detail="Usage not found")
        return db_usage


def add_read_all_routes(app: FastAPI):
    @app.get("/errors/", response_model=List[schemas.Error])
    def read_errors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        errors = crud.get_errors(db, skip=skip, limit=limit)
        return errors

    @app.get("/usages/", response_model=List[schemas.Usage])
    def read_usages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        usages = crud.get_usages(db, skip=skip, limit=limit)
        return usages

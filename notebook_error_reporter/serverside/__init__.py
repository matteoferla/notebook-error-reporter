from fastapi import FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas, routes
from .database import SessionLocal, engine, get_db

def create_db():
    models.Base.metadata.create_all(bind=engine)

def create_app(debug:bool=False, max_transparency:bool=True) -> FastAPI:
    app = FastAPI(debug=debug)
    routes.add_create_routes(app)
    routes.add_read_one_routes(app)
    if max_transparency:
        routes.add_read_all_routes(app)
    return app
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
import uuid
import os, json, sys
from datetime import datetime, timedelta
from functools import singledispatch

def assert_not_bloated(cutoff=1e10):
    """
    Is the database larger than 10 MB?
    """
    if os.path.getsize('error.db') > 1e10:
        return HTTPException(418, 'Sorry, someone has been an arse and clogged up the server')

@singledispatch
def get_usage(usage_uuid: str, db: Session):
    return db.query(models.Usage).filter(models.Usage.uuid == usage_uuid).first()


@get_usage.register
def _(usage_id: int, db: Session):  # vanilla just in case.
    return db.query(models.Usage).filter(models.Usage.id == usage_id).first()

def get_usages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usage).offset(skip).limit(limit).all()

def get_usages_by_ip(db: Session, ip: str):
    return db.query(models.Usage).filter(models.Usage.ip == ip).all()

def create_usage(db: Session,
                 usage: schemas.UsageCreate,
                 ip:str):
    """
    The timestamp is set by the database.
    """
    usages_for_ip = get_usages_by_ip(db, ip)
    assert_not_bloated()
    if usages_for_ip and len(usages_for_ip) > 100:
        return HTTPException(429, 'Stop trying to vandalise! Your VM has already done a hundred sessions...')
    elif sys.getsizeof(json.dumps(usage.dict())) > 1e3:  # Pointless as Apache or Nginx limit is in place...
        return HTTPException(429, 'Stop trying to vandalise! Your session is over 1 MB?')
    else:
        pass
    db_usage = models.Usage(notebook=usage.notebook, ip=ip, uuid=uuid.uuid4().hex)
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage


def get_errors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Error).offset(skip).limit(limit).all()


def create_error(db: Session, error: schemas.ErrorCreate, usage_uuid: str, ip: str):
    usage = get_usage(usage_uuid, db=db)
    assert_not_bloated()
    if usage is None or usage.ip != ip:
        raise HTTPException(status_code=403, detail="IP address differs")
    elif len(usage.errors) > 100:
        return HTTPException(429, 'Stop trying to vandalise! Your session has already done a hundred errors...')
    elif len(usage.errors) and datetime.now() - usage.errors[-1].timestamp < timedelta(seconds=5):
        return HTTPException(429, 'Stop trying to vandalise! You raise an error less than 5 seconds ago...')
    elif sys.getsizeof(json.dumps(error.dict())) > 1e4:  # Pointless as Apache or Nginx limit is in place...
        return HTTPException(429, 'Stop trying to vandalise! Your error is over 10 MB?')
    else:
        pass  # legitimate.
    db_error = models.Error(**error.dict(), usage_uuid=usage_uuid)
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    return db_error

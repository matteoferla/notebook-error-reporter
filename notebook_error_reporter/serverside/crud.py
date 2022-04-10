from sqlalchemy.orm import Session
from fastapi import HTTPException
from error_reporting_backend import models, schemas
import uuid
from functools import singledispatch

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
    if len(usages_for_ip) > 1_000:
        return HTTPException(429, 'This VM has already done a thousand requests...')
    db_usage = models.Usage(notebook=usage.notebook, ip=ip, uuid=uuid.uuid4().hex)
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage


def get_errors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Error).offset(skip).limit(limit).all()


def create_error(db: Session, error: schemas.ErrorCreate, usage_uuid: str, ip: str):
    usage = get_usage(usage_uuid, db=db)
    if usage is None or usage.ip != ip:
        raise HTTPException(status_code=403, detail="IP address differs")
    db_error = models.Error(**error.dict(), usage_uuid=usage_uuid)
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    return db_error

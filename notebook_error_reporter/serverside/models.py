from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from error_reporting_backend.database import Base


class Error(Base):
    __tablename__ = "errors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usage_uuid = Column(String, ForeignKey("usages.uuid"))
    name = Column(String)  # type is a builtin
    message = Column(String)
    traceback = Column(JSON)
    execution_count = Column(Integer)
    first_line = Column(String)
    time = Column(DateTime(timezone=True), server_default=func.now())
    usage = relationship("Usage", back_populates="errors")

class Usage(Base):
    """
    It's a notebook session not a user, but session is also db session.
    """
    __tablename__ = "usages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String, unique=True)
    ip = Column(String)  # not unique, maybe.
    notebook = Column(String)
    time = Column(DateTime(timezone=True), server_default=func.now())
    errors = relationship("Error", back_populates="usage")

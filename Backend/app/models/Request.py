from sqlalchemy import String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship
import datetime
from . import ModelBase
from .HttpMethod import HttpMethod

class Request(ModelBase):

    __tablename__ = "requests"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    session_id = mapped_column(Integer(), ForeignKey("sessions.id"))
    cookies = mapped_column(String(1000))
    headers = mapped_column(String(1000))
    data = mapped_column(String(1000))
    url = mapped_column(String(150))
    time = mapped_column(DateTime(), default=datetime.datetime.now)
    method = mapped_column(Enum(HttpMethod), default=HttpMethod.GET)

    response = relationship("Response", back_populates="request")
    session = relationship("DbSession", back_populates="requests", uselist=False)
from sqlalchemy import DateTime, Integer, ForeignKey, Enum, Text
from sqlalchemy.orm import mapped_column, relationship
import datetime
from . import ModelBase
from .HttpMethod import HttpMethod

class Request(ModelBase):

    __tablename__ = "requests"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    session_id = mapped_column(Integer(), ForeignKey("sessions.id"))
    cookies = mapped_column(Text())
    headers = mapped_column(Text())
    data = mapped_column(Text())
    url = mapped_column(Text())
    time = mapped_column(DateTime(), default=datetime.datetime.now)
    method = mapped_column(Enum(HttpMethod), default=HttpMethod.GET)

    response = relationship("Response", back_populates="request", uselist=False)
    session = relationship("DbSession", back_populates="requests", uselist=False)
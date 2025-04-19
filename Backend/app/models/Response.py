from sqlalchemy import DateTime, Integer, ForeignKey, Enum, Text
from sqlalchemy.orm import mapped_column, relationship
import datetime
from . import ModelBase
from .HttpMethod import HttpMethod

class Response(ModelBase):

    __tablename__ = "responses"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    request_id = mapped_column(Integer(), ForeignKey("requests.id"))
    session_id = mapped_column(Integer(), ForeignKey("sessions.id"))
    cookies = mapped_column(Text())
    headers = mapped_column(Text())
    data = mapped_column(Text())
    url = mapped_column(Text())
    time = mapped_column(DateTime(), default=datetime.datetime.now)
    method = mapped_column(Enum(HttpMethod), default=HttpMethod.GET)

    request = relationship("Request", back_populates="response")
    session = relationship("DbSession", back_populates="responses")

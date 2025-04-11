from sqlalchemy import String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship
import datetime
from main import Base
from HttpMethod import HttpMethod

class Response(Base):

    __tablename__ = "responses"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    request_id = mapped_column(Integer(), ForeignKey("requests.id"))
    session_id = mapped_column(Integer(), ForeignKey("sessions.id"))
    cookies = mapped_column(String(1000))
    headers = mapped_column(String(1000))
    data = mapped_column(String(1000))
    url = mapped_column(String(150))
    time = mapped_column(DateTime(), default=datetime.datetime.now)
    method = mapped_column(Enum(HttpMethod), default=HttpMethod.GET)

    request = relationship("Request", back_populates="response")
    session = relationship("DbSession", back_populates="responses")

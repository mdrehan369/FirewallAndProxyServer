from sqlalchemy import String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, relationship
from .main import Base
import datetime

class DbSession(Base):

    __tablename__ = "sessions"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    employee_corporate_id = mapped_column(String(10), ForeignKey("employees.corporate_id"), nullable=False)
    loggedin_at = mapped_column(DateTime(), default=datetime.datetime.now)
    loggedout_at = mapped_column(DateTime(), default=datetime.datetime.now)
    did_logged_out = mapped_column(Boolean(), default=False)
    system_ip = mapped_column(String(15), nullable=False)

    employee = relationship("Employee", back_populates="sessions")
    requests = relationship("Request", back_populates="session", uselist=True)
    responses = relationship("Response", back_populates="session", uselist=True)
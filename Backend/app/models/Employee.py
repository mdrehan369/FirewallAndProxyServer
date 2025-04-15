from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, relationship
import datetime
import random
from . import ModelBase

def createUniqueIds():
    uuid = ""
    for i in range(0, 10):
        uuid += "abcdefghijklmnopqrstuvwxyz"[random.randint(0, 25)]
    return uuid

class Employee(ModelBase):

    __tablename__ = "employees"

    corporate_id = mapped_column(String(10), primary_key=True, default=createUniqueIds)
    corporate_password = mapped_column(String(15), nullable=False)
    fullname = mapped_column(String(30), nullable=False)
    role = mapped_column(String(50), nullable=False)
    email = mapped_column(String(50), nullable=False)
    joined_at = mapped_column(DateTime(), default=datetime.datetime.now)

    sessions = relationship("DbSession", back_populates="employee", uselist=True)

from sqlalchemy import Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import mapped_column, DeclarativeBase, relationship, create_session

import asyncio
import os
import random
import datetime

def createUniqueIds():
    uuid = ""
    for i in range(0, 10):
        uuid += "abcdefghijklmnopqrstuvwxyz"[random.randint(0, 26)]
    return uuid

class Base(DeclarativeBase):
    pass

class Employee(Base):

    _tablename_ = "employees"

    corporate_id = mapped_column(String(10), primary_key=True, default=createUniqueIds)
    fullname = mapped_column(String(30), nullable=False)
    system_ip = mapped_column(String(15), nullable=False, unique=True)

    joined_at = mapped_column(DateTime, default=datetime.datetime.now)

    attendances = relationship("attendances", back_populates=True)


def createUniqueIds():
    uuid = ""
    for i in range(0, 10):
        uuid += "abcdefghijklmnopqrstuvwxyz"[random.randint(0, 26)]
    return uuid

class Base(DeclarativeBase):
    pass

class Employee(Base):

    _tablename_ = "employees"

    corporate_id = mapped_column(String(10), primary_key=True, default=createUniqueIds)
    fullname = mapped_column(String(30), nullable=False)
    system_ip = mapped_column(String(15), nullable=False, unique=True)

    joined_at = mapped_column(DateTime, default=datetime.datetime.now)

    attendances = relationship("attendances", back_populates=True)



class Attendance(Base):

    _tablename_ = "attendances"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    employee_corporate_id = mapped_column(String(10), ForeignKey("employees.corporate_id"), nullable=False)
    login_at = mapped_column(DateTime(), default=datetime.datetime.now)
    logout_at = mapped_column(DateTime(), default=datetime.datetime.now)

class IpTable(Base):

    _tablename_ = "iptables"

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    ip = mapped_column(String(15), ForeignKey("employees.system_ip"))
    ports = mapped_column(Integer(), default=1)

databaseUrl = os.environ.get("DATABASE_URL")

engine = create_engine(databaseUrl)

Base.metadata.create_all(engine)

Session = create_session(engine)
session = Session()

async def addAttendance(system_ip):
    global session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from models import Employee, Response, Request, DbSession
from ..models.DbSession import DbSession
from ..models.Employee import Employee
from datetime import datetime

import os
from dotenv import load_dotenv
from ..models import ModelBase

from .CustomResponse import CustomResponse


load_dotenv()
class DbHelper():

    databaseUrl = ""
    engine = None
    session = None

    def __init__(self):
        self.databaseUrl = os.getenv("DATABASE_URL")
        self.engine = create_engine(self.databaseUrl, echo=True)
        ModelBase.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)

        print("Database created!")
        print("DB Helper Initialized!")

    def checkEmployeeSession(self, system_ip):
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            existingSession = session.query(DbSession).filter(DbSession.system_ip == system_ip, DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00").all()
            print(existingSession)
            if(len(existingSession) == 0):
                return CustomResponse(success=False, data={ "status": False }).toJson()
            return CustomResponse(success=True, data={ "status": True }).toJson()

    def loginEmployee(self, corporate_id, corporate_password, system_ip):
        if corporate_id == "" or corporate_password == "":
            return CustomResponse(success=False, message="Credentials Missing")
        with self.session() as session:
            employee = session.query(Employee).filter(Employee.corporate_id == corporate_id).first()
            if employee == None:
                return CustomResponse(success=False, message="No Employee Found")
            
            if employee.corporate_password != corporate_password:
                return CustomResponse(success=False, message="Invalid Credentials")
            
            session.add(DbSession(employee_corporate_id=corporate_id, system_ip=system_ip))
            session.commit()

            return CustomResponse(success=True, message="Session Created Successfully!", status=201)
            


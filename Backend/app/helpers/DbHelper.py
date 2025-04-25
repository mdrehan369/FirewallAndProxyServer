from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
# from models import Employee, Response, Request, DbSession
from ..models.DbSession import DbSession
from ..models.Employee import Employee
from ..models.Request import Request
from ..models.Response import Response
from ..models.HttpMethod import HttpMethod
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
        self.engine = create_engine(self.databaseUrl, echo=False)
        ModelBase.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)

        print("Database created!")
        print("DB Helper Initialized!")

    def _findCurrSession(self, system_ip):
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            existingSession = session.query(DbSession).filter(DbSession.system_ip == system_ip, DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00", DbSession.did_logged_out == False).first()
            return existingSession


    def checkEmployeeSession(self, system_ip):
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            existingSession = session.query(DbSession).filter(DbSession.system_ip == system_ip, DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00", DbSession.did_logged_out == False).all()
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
            

    def getEmployee(self, system_ip: str):
        if system_ip == "":
            return CustomResponse(success=False, message="No IP Given!")
        
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year
        
        with self.session() as session:
            dbSession = session.query(DbSession).filter(DbSession.system_ip == system_ip, DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00", DbSession.did_logged_out == False).first()
            if dbSession is None:
                return CustomResponse(success=False, message="No Session Found!")
            employee = dbSession.employee
            if employee is None:
                return CustomResponse(success=False, message="No Employee Found!")
            return CustomResponse(data=employee)
        
    def logoutEmployee(self, system_ip: str):
        if system_ip == "":
            return CustomResponse(success=False, message="No IP Given!")
        
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year
        
        with self.session() as session:
            dbSession = session.query(DbSession).filter(DbSession.system_ip == system_ip, DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00", DbSession.did_logged_out == False).first()

            if dbSession is None:
                return CustomResponse(success=False, message="No Employe Found!")
            session.execute(
                (
                    update(DbSession)
                    .where(DbSession.system_ip == system_ip, DbSession.did_logged_out == False, DbSession.loggedin_at >= datetime(year, month, date))
                    .values(did_logged_out=True, loggedout_at=datetime.now())
                    )
                )
            
            session.commit()
            return CustomResponse()
        
    def addRequest(self, cookies: str, headers: str, data: str, url: str, method: HttpMethod, system_ip: str):
        existingSession = self._findCurrSession(system_ip)
        if existingSession is None:
            return CustomResponse(success=False, message="No Session Found!")
        # request = None
        id = 10
        with self.session() as session:
            request = Request(cookies=cookies, headers=headers, data=data, url=url, method=method, session_id=existingSession.id)
            session.add(request)
            session.commit()
            id = request.id
        return CustomResponse(data=id)
    
    def addResponse(self, cookies: str, headers: str, data: str, url: str, method: HttpMethod, system_ip: str):
        existingSession = self._findCurrSession(system_ip)
        if existingSession is None:
            return CustomResponse(success=False, message="No Session Found!")
        # response = None
        id = None
        with self.session() as session:
            request = session.query(Request).where(Request.url == url, Request.method == method, Request.session_id == existingSession.id, Request.response == None).first()
            if request is None:
                return CustomResponse(success=False, message="No Request Found!")
            response = Response(cookies=cookies, headers=headers, data=data, url=url, method=method, session_id=existingSession.id, request=request)
            session.add(response)
            session.commit()
            id = response.id
        return CustomResponse(data=id)
    
    def getRequestById(self, id: str):
        if id is None:
            return CustomResponse(success=False, message="No ID Found!")
        
        with self.session() as session:
            request = session.query(Request).where(Request.id == id).first()
            # Lazy Loading Other Tables Data
            request.session
            request.response
            request.response.session
            request.session.employee
            if request is None:
                return CustomResponse(status=404, message="Request Not Found!", success=False)
            return request
        
    def getResponseById(self, id: str):
        if id is None:
            return CustomResponse(success=False, message="No ID Found!")
        
        with self.session() as session:
            response = session.query(Response).where(Response.id == id).first()
            # Lazy Loading Other Tables Data
            response.session
            response.request
            response.request.session
            response.session.employee
            if response is None:
                return CustomResponse(status=404, message="Response Not Found!", success=False)
            return response
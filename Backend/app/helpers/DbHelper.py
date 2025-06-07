from typing import Any, Dict, List
from sqlalchemy import create_engine, update, or_, desc
from sqlalchemy.orm import sessionmaker, selectinload

# from models import Employee, Response, Request, DbSession
from ..models.DbSession import DbSession
from ..models.Employee import Employee
from ..models.Request import Request, RequestOut
from ..models.Response import Response
from ..models.HttpMethod import HttpMethod
from datetime import datetime

import os
from dotenv import load_dotenv
from ..models import ModelBase

from .CustomResponse import CustomResponse
from ..types.EmployeePost import EmployeePostBody

load_dotenv()


class DbHelper:

    databaseUrl = ""
    engine = None
    # session: sessionmaker | None = None

    def __init__(self):
        self.databaseUrl = os.getenv("DATABASE_URL")
        self.engine = create_engine(self.databaseUrl or "", echo=False)
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
            existingSession = (
                session.query(DbSession)
                .filter(
                    DbSession.system_ip == system_ip,
                    DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00",
                    DbSession.did_logged_out == False,
                )
                .first()
            )
            return existingSession

    def checkEmployeeSession(self, system_ip):
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            existingSession = (
                session.query(DbSession)
                .filter(
                    DbSession.system_ip == system_ip,
                    DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00",
                    DbSession.did_logged_out == False,
                )
                .all()
            )
            if len(existingSession) == 0:
                return CustomResponse(success=False, data={"status": False}).toJson()
            return CustomResponse(success=True, data={"status": True}).toJson()

    def loginEmployee(
        self, corporate_id, corporate_password, system_ip
    ) -> Dict[str, Any]:
        if corporate_id == "" or corporate_password == "":
            return {"success": False, "message": "Credentials Missing"}
        with self.session() as session:
            employee = (
                session.query(Employee)
                .filter(Employee.corporate_id == corporate_id)
                .first()
            )
            if employee == None:
                return {"success": False, "message": "No employee found"}

            if employee.corporate_password != corporate_password:
                return {"success": False, "message": "Invalid Credentials"}

            session.add(
                DbSession(employee_corporate_id=corporate_id, system_ip=system_ip)
            )
            session.commit()

            return {"success": True, "message": "Employee logged in successfully!"}

    def getEmployee(self, system_ip: str):
        if system_ip == "":
            return {"success": False, "message": "No IP given"}
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            dbSession = (
                session.query(DbSession)
                .filter(
                    DbSession.system_ip == system_ip,
                    DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00",
                    DbSession.did_logged_out == False,
                )
                .first()
            )
            if dbSession is None:
                return {"success": False, "message": "No session found"}
            employee = dbSession.employee
            if employee is None:
                return {"success": False, "message": "No employee found"}
            return {"success": True, "message": "Done", "data": employee}

    def logoutEmployee(self, system_ip: str):
        if system_ip == "":
            return {"success": False, "message": "No IP given"}

        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            dbSession = (
                session.query(DbSession)
                .filter(
                    DbSession.system_ip == system_ip,
                    DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00",
                    DbSession.did_logged_out == False,
                )
                .first()
            )

            if dbSession is None:
                return {"success": False, "message": "No employee found"}

            session.execute(
                (
                    update(DbSession)
                    .where(
                        DbSession.system_ip == system_ip,
                        DbSession.did_logged_out == False,
                        DbSession.loggedin_at >= datetime(year, month, date),
                    )
                    .values(did_logged_out=True, loggedout_at=datetime.now())
                )
            )

            session.commit()
            return {"success": True, "message": "Done"}

    def addRequest(
        self,
        cookies: str,
        headers: str,
        data: str,
        url: str,
        method: HttpMethod,
        system_ip: str,
    ):
        existingSession = self._findCurrSession(system_ip)
        if existingSession is None:
            return CustomResponse(success=False, message="No Session Found!")
        # request = None
        id = 10
        with self.session() as session:
            request = Request(
                cookies=cookies,
                headers=headers,
                data=data,
                url=url,
                method=method,
                session_id=existingSession.id,
            )
            session.add(request)
            session.commit()
            id = request.id
        return CustomResponse(data=id)

    def addResponse(
        self,
        cookies: str,
        headers: str,
        data: str,
        url: str,
        method: HttpMethod,
        system_ip: str,
    ):
        existingSession = self._findCurrSession(system_ip)
        if existingSession is None:
            return CustomResponse(success=False, message="No Session Found!")
        # response = None
        id = None
        with self.session() as session:
            request = (
                session.query(Request)
                .where(
                    Request.url == url,
                    Request.method == method,
                    Request.session_id == existingSession.id,
                    Request.response == None,
                )
                .first()
            )
            if request is None:
                return CustomResponse(success=False, message="No Request Found!")
            response = Response(
                cookies=cookies,
                headers=headers,
                data=data,
                url=url,
                method=method,
                session_id=existingSession.id,
                request=request,
            )
            session.add(response)
            session.commit()
            id = response.id
        return CustomResponse(data=id)

    def getRequestById(self, id: str):

        with self.session() as session:
            request = session.query(Request).where(Request.id == id).first()
            if request is None:
                return None
            # Lazy Loeding Other Tables Data
            request.session
            request.response
            request.response.session
            request.session.employee

            return RequestOut.from_orm(request)

    def getResponseById(self, id: str):
        with self.session() as session:
            response = session.query(Response).where(Response.id == id).first()
            if response is None:
                return None
            # Lazy Loading Other Tables Data
            response.session
            response.request
            response.request.session
            response.session.employee
            return CustomResponse(data=response)

    def getAllEmployees(self, page: int, limit: int, search: str) -> List[Employee]:
        with self.session() as session:
            query = session.query(Employee)
            if search != "":
                query = query.filter(
                    or_(
                        Employee.corporate_id.startswith(f"{search}"),
                        Employee.fullname.startswith(f"{search}"),
                        Employee.email.startswith(f"{search}"),
                    )
                )

            employees = query.offset((page - 1) * limit).limit(limit).all()
            return employees

    def addEmployee(self, employee: EmployeePostBody):
        with self.session() as session:
            isEmployeeExists = (
                session.query(Employee).filter(Employee.email == employee.email).first()
            )
            if isEmployeeExists is not None:
                return False
            session.add(
                Employee(
                    email=employee.email,
                    corporate_password=employee.corporate_password,
                    role=employee.role,
                    fullname=employee.fullname,
                )
            )
            session.commit()
            return True

    def deleteEmployee(self, id: str):
        with self.session() as session:
            employee = (
                session.query(Employee).filter(Employee.corporate_id == id).first()
            )
            if employee is None:
                return False

            session.delete(employee)
            session.commit()

        return True

    def getAllSessions(self, page: int = 1, limit: int = 15):
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            allSessions = {}
            allSessions["active"] = (
                session.query(DbSession)
                .filter(
                    DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00",
                    DbSession.did_logged_out == False,
                )
                .order_by(desc(DbSession.loggedin_at))
                .offset((page - 1) * limit)
                .limit(limit)
                .options(selectinload(DbSession.employee))
                .all()
            )

            allSessions["inactive"] = (
                session.query(DbSession)
                .filter(
                    or_(
                        DbSession.loggedin_at < f"{year}-{month}-{date} 00:00:00",
                        DbSession.did_logged_out == True,
                    )
                )
                .order_by(desc(DbSession.loggedin_at))
                .offset((page - 1) * limit)
                .limit(limit)
                .options(selectinload(DbSession.employee))
                .all()
            )

            return allSessions

    def getSessionsRequest(self, session_id: int):
        with self.session() as session:
            dbSession = (
                session.query(DbSession).where(DbSession.id == session_id).first()
            )
            if dbSession is None:
                return None
            dbSession.employee
            dbSession.requests
            dbSession.responses

            return dbSession

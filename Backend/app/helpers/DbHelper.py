from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from models import Employee, Response, Request, DbSession
from models.DbSession import DbSession
from datetime import datetime

import os

class DbHelper():

    databaseUrl = ""
    engine = None
    session = None

    def __init__(self):
        self.databaseUrl = os.getenv("DATABASE_URL")
        self.engine = create_engine(self.databaseUrl, echo=True)
        self.session = sessionmaker(bind=self.engine)
        print("DB Helper Initialized!")

    def checkEmployeeSession(self, system_ip):
        currTime = datetime.now()
        date = currTime.day
        month = currTime.month
        year = currTime.year

        with self.session() as session:
            existingSession = session.query(DbSession).filter(DbSession.system_ip == system_ip, DbSession.loggedin_at >= f"{year}-{month}-{date} 00:00:00").all()
            print(existingSession)
            # if existingSession == None:
            #     print("No session found!")
            # else:
            #     print("session found")

from Backend.app.models import engine, Employee, DbSession, Request, Response
from sqlalchemy.orm import sessionmaker

from faker import Faker

job_roles = [
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Mobile App Developer",
    "QA Engineer",
    "Machine Learning Engineer",
    "Data Engineer",
    "Security Engineer",
    "Site Reliability Engineer",
    "Cloud Engineer",
    "Software Architect",
    "Game Developer",
    "Embedded Systems Engineer",
    "Software Engineer"
  ]

Session = sessionmaker(bind=engine)
fake = Faker()

def createEmployee():
    corporate_password = "1234"
    fullname = fake.name()
    role = job_roles[fake.random_int(min=0, max=len(job_roles) - 1)]
    email = fake.email()

    return Employee(corporate_password=corporate_password, fullname=fullname, role=role, email=email)

with Session() as session:

    for i in range(0, 15):
        employee = createEmployee()
        session.add(employee)
        
    session.commit()

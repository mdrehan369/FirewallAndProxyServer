from pydantic import BaseModel

class EmployeePostBody(BaseModel):
    fullname: str
    corporate_password: str
    role: str
    email: str
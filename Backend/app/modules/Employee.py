from fastapi import APIRouter, Request, Response, status
from ..utils import dbHelperInstance
from ..types.EmployeePost import EmployeePostBody

router = APIRouter(prefix="/employee")

@router.get("/")
def getEmployees(req: Request, page: int = 1, limit: int = 15, search: str = ""):
    return dbHelperInstance.getAllEmployees(page=page, limit=limit, search=search)

@router.post("/")
def addEmployee(req: Request, employee: EmployeePostBody):
    return dbHelperInstance.addEmployee(employee)

@router.delete("/{id}")
def deleteEmployee(req: Request, id: str):
    return dbHelperInstance.deleteEmployee(id)

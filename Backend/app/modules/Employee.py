from fastapi import APIRouter, Request, Response, status
from ..utils import dbHelperInstance
from ..types.EmployeePost import EmployeePostBody

router = APIRouter(prefix="/employee")

@router.get("/")
def getEmployees(req: Request, page: int = 1, limit: int = 15, search: str = ""):
    return dbHelperInstance.getAllEmployees(page=page, limit=limit, search=search)

@router.post("/")
def addEmployee(req: Request, employee: EmployeePostBody):
    response = dbHelperInstance.addEmployee(employee)
    if response.success == False:
        return Response(content="User already exists" ,status_code=status.HTTP_400_BAD_REQUEST)
    return response
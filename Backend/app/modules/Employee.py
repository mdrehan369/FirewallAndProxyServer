from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse

from app.helpers.CustomResponse import CustomResponse
from ..utils import dbHelperInstance
from ..types.EmployeePost import EmployeePostBody

router = APIRouter(prefix="/employee")


@router.get("/")
def getEmployees(req: Request, page: int = 1, limit: int = 15, search: str = ""):
    employees = dbHelperInstance.getAllEmployees(page=page, limit=limit, search=search)
    return JSONResponse(
        content=CustomResponse(data=employees), status_code=status.HTTP_200_OK
    )


@router.post("/")
def addEmployee(req: Request, employee: EmployeePostBody):
    response = dbHelperInstance.addEmployee(employee)
    if response == False:
        return JSONResponse(
            content=CustomResponse(
                status=400, message="User already exists", success=False
            ),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content=CustomResponse(status=201), status_code=status.HTTP_201_CREATED
    )


@router.delete("/{id}")
def deleteEmployee(req: Request, id: str):
    response = dbHelperInstance.deleteEmployee(id)
    if response == False:
        return JSONResponse(
            content=CustomResponse(status=404, success=False, message="User not found"),
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return JSONResponse(
        content=CustomResponse(status=200), status_code=status.HTTP_200_OK
    )

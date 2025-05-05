from fastapi import APIRouter, Request
from ..utils import dbHelperInstance
from ..helpers.CustomResponse import CustomResponse

router = APIRouter(prefix="/session")

@router.get("/")
def getAllSessions(req: Request, page: int = 1, limit: int = 15):
    response = dbHelperInstance.getAllSessions()
    return CustomResponse(data=response)
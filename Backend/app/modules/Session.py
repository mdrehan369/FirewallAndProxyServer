from fastapi import APIRouter, Request, responses
from ..utils import dbHelperInstance
from ..helpers.CustomResponse import CustomResponse

router = APIRouter(prefix="/session")

@router.get("/")
def getAllSessions(req: Request, page: int = 1, limit: int = 15):
    response = dbHelperInstance.getAllSessions()
    return CustomResponse(data=response)

@router.get("/{session_id}")
def getSessionRequests(req: Request, session_id: int):
    response = dbHelperInstance.getSessionsRequest(session_id)
    return response

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from ..utils import dbHelperInstance
from ..helpers.CustomResponse import CustomResponse

router = APIRouter(prefix="/session")


@router.get("/")
def getAllSessions(req: Request, page: int = 1, limit: int = 15):
    response = dbHelperInstance.getAllSessions(page=page, limit=limit)
    return JSONResponse(
        content=CustomResponse(data=response), status_code=status.HTTP_200_OK
    )


@router.get("/{session_id}")
def getSessionRequests(req: Request, session_id: int):
    response = dbHelperInstance.getSessionsRequest(session_id)
    if response is None:
        return JSONResponse(
            content=CustomResponse(
                success=False, status=404, message="Session not found"
            ),
            status_code=HTTP_404_NOT_FOUND,
        )
    return JSONResponse(content=CustomResponse(data=response), status_code=HTTP_200_OK)

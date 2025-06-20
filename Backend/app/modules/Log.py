from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.helpers.CustomResponse import CustomResponse
from ..utils import dbHelperInstance

router = APIRouter(prefix="/log")


@router.get("/request/{id}")
async def getLogByIdRequest(req: Request, id: str):
    response = dbHelperInstance.getRequestById(id)
    if response is None:
        return CustomResponse(
            status=404, message="Request not found", success=False
        ).to_json_response()

    return response


@router.get("/response/{id}")
async def getLogByIdResponse(req: Request, id: str):
    response = dbHelperInstance.getResponseById(id)
    # print(response)
    if response is None:
        return CustomResponse(
            status=404, message="Response not found", success=False
        ).to_json_response()

    return response

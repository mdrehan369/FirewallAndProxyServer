from fastapi import APIRouter, Request
from ..utils import dbHelperInstance

router = APIRouter(prefix="/log")

@router.get("/request/{id}")
async def getLogByIdRequest(req: Request, id: str):
    return dbHelperInstance.getRequestById(id)

@router.get("/response/{id}")
async def getLogByIdResponse(req: Request, id: str):
    return dbHelperInstance.getResponseById(id)

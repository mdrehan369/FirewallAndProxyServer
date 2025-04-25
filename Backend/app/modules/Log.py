from fastapi import APIRouter, Request
from ..utils import dbHelperInstance

router = APIRouter(prefix="/log")

@router.get("/request/{id}")
async def getLogById(req: Request, id: str):
    return dbHelperInstance.getRequestById(id)

@router.get("/response/{id}")
async def getLogById(req: Request, id: str):
    return dbHelperInstance.getResponseById(id)
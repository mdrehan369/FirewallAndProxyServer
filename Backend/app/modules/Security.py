from fastapi import APIRouter, Request
from ..utils import templates

router = APIRouter(prefix="/security")


@router.get("/threat")
def showThreat(req: Request):
    url = req.cookies.get("url")
    return templates.TemplateResponse(
        req, name="RiskWarning.html", context={"url": url}
    )


@router.get("/warn")
def showWarning(req: Request):
    url = req.cookies.get("url")
    return templates.TemplateResponse(
        req, name="SuspiciousWarning.html", context={"url": url}
    )

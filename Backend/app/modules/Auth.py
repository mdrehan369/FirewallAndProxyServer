from os import name
from fastapi import APIRouter
from fastapi import Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Annotated
from ..utils import templates, dbHelperInstance

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse(request=req, name="Login.html")


@router.post("/login")
async def loginPost(
    req: Request,
    corporate_id: Annotated[str, Form()],
    corporate_password: Annotated[str, Form()],
):

    system_ip = req.cookies.get("system_ip")
    url = req.cookies.get("url")
    if url is None or system_ip is None:
        return
    response = dbHelperInstance.loginEmployee(
        corporate_id=corporate_id,
        corporate_password=corporate_password,
        system_ip=system_ip,
    )
    if response["success"] == False:
        return templates.TemplateResponse(
            request=req, name="Login.html", context={"error": response["message"]}
        )
    return RedirectResponse(url=url)


@router.get("/logout")
async def logout(req: Request):
    system_ip = req.client.host  # type: ignore
    response = dbHelperInstance.getEmployee(system_ip)
    if response["success"]:
        return templates.TemplateResponse(
            request=req,
            name="Logout.html",
            context={"employee": response["data"], "system_ip": system_ip},
        )
    return templates.TemplateResponse(
        request=req, name="Logout.html", context={"error": response["message"]}
    )


@router.post("/logout")
async def logoutEmployee(req: Request):
    system_ip = req.client.host  # type: ignore
    response = dbHelperInstance.logoutEmployee(system_ip)
    if response["success"]:
        return templates.TemplateResponse(
            request=req, name="Logout.html", context={"success": True}
        )
    return templates.TemplateResponse(
        request=req, name="Logout.html", context={"error": response["message"]}
    )


@router.get("/limit-reached")
async def limitReached(req: Request):
    return templates.TemplateResponse(request=req, name="Limit.html")

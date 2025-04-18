from fastapi import APIRouter
from fastapi import Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Annotated
from ..utils import templates, dbHelperInstance

class Auth:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/login", endpoint=self.login, response_class=HTMLResponse, methods=["GET"])
        self.router.add_api_route("/login", endpoint=self.loginPost, methods=["POST"])
        self.router.add_api_route("/logout", endpoint=self.logout, methods=["GET"], response_class=HTMLResponse)
        self.router.add_api_route("/logout", endpoint=self.logoutEmployee, methods=["POST"])

    # @app.get("/login", response_class=HTMLResponse)
    async def login(req: Request):
        return templates.TemplateResponse(
            request=req, name="Login.html"
        )


    # @app.post("/login")
    async def loginPost(req: Request, corporate_id: Annotated[str, Form()], corporate_password: Annotated[str, Form()]):

        system_ip = req.cookies.get("system_ip")
        url = req.cookies.get("url")
        response = dbHelperInstance.loginEmployee(corporate_id=corporate_id, corporate_password=corporate_password, system_ip=system_ip)
        if response.success == False:
            return templates.TemplateResponse(
            request=req, name="Login.html", context={"error": response.message}
        )
        return RedirectResponse(url=url)

    # @app.get("/logout")
    async def logout(req: Request):
        system_ip = req.client.host
        response = dbHelperInstance.getEmployee(system_ip)
        if response.success:
            return templates.TemplateResponse(
                request=req, name="Logout.html", context={ "employee": response.data, "system_ip": system_ip }
            )
        return templates.TemplateResponse(
                request=req, name="Logout.html", context={ "error": response.message }
            )

    # @app.post("/logout")
    async def logoutEmployee(req: Request):
        system_ip = req.client.host
        response = dbHelperInstance.logoutEmployee(system_ip)
        if response.success:
            return templates.TemplateResponse(
                    request=req, name="Logout.html", context={ "success": True }
                )
        return templates.TemplateResponse(
                request=req, name="Logout.html", context={ "error": response.message }
            )

auth = Auth()
authRouter = auth.router
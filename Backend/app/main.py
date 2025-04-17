from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import json
from .helpers.DbHelper import DbHelper
from typing import Annotated
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join(os.getcwd(), "app/templates"))
dbHelper = DbHelper()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def homeRoute():
    return { "message": "hello world!" }


@app.get("/login", response_class=HTMLResponse)
async def login(req: Request):
    return templates.TemplateResponse(
        request=req, name="Login.html"
    )


@app.post("/login")
async def loginPost(req: Request, corporate_id: Annotated[str, Form()], corporate_password: Annotated[str, Form()]):

    system_ip = req.cookies.get("system_ip")
    url = req.cookies.get("url")
    response = dbHelper.loginEmployee(corporate_id=corporate_id, corporate_password=corporate_password, system_ip=system_ip)
    if response.success == False:
        return templates.TemplateResponse(
        request=req, name="Login.html", context={"error": response.message}
    )
    return RedirectResponse(url=url)

@app.get("/logout")
async def logout(req: Request):
    system_ip = req.client.host
    response = dbHelper.getEmployee(system_ip)
    if response.success:
        return templates.TemplateResponse(
            request=req, name="Logout.html", context={ "employee": response.data, "system_ip": system_ip }
        )
    return templates.TemplateResponse(
            request=req, name="Logout.html", context={ "error": response.message }
        )

@app.post("/logout")
async def logoutEmployee(req: Request):
    system_ip = req.client.host
    response = dbHelper.logoutEmployee(system_ip)
    if response.success:
        return templates.TemplateResponse(
                request=req, name="Logout.html", context={ "success": True }
            )
    return templates.TemplateResponse(
            request=req, name="Logout.html", context={ "error": response.message }
        )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            if(data["method"] == "CHECK_EMPLOYEE_STATUS"):
                session = dbHelper.checkEmployeeSession(data["data"]["system_ip"])
                await websocket.send_text(session)

    except WebSocketDisconnect:
        print(f"Client left the chat")
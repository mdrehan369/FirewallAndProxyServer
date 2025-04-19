from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .modules.Auth import router as authRouter

import json
from .utils import dbHelperInstance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRouter)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            if(data["method"] == "CHECK_EMPLOYEE_STATUS"):
                session = dbHelperInstance.checkEmployeeSession(data["data"]["system_ip"])
                await websocket.send_text(session)

            elif(data["method"] == "ADD_REQUEST"):
                requestData = data["data"]
                response = dbHelperInstance.addRequest(cookies=requestData["cookies"], headers=requestData["headers"], data=requestData["data"], method=requestData["method"], system_ip=requestData["system_ip"], url=requestData["url"])
                print(response)

            elif(data["method"] == "ADD_RESPONSE"):
                responseData = data["data"]
                response = dbHelperInstance.addResponse(cookies=responseData["cookies"], headers=responseData["headers"], data=responseData["data"], method=responseData["method"], system_ip=responseData["system_ip"], url=responseData["url"])
                print(response)

    except WebSocketDisconnect:
        print(f"Client left the chat")
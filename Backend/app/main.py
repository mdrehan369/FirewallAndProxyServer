from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .modules.Auth import authRouter

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

    except WebSocketDisconnect:
        print(f"Client left the chat")
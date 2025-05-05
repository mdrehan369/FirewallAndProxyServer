from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .modules.Auth import router as authRouter
from .modules.Log import router as logRouter
from .modules.Employee import router as employeeRouter
from .modules.Session import router as sessionRouter
import logging
import json
from .utils import dbHelperInstance, redisHelperInstance
from typing import List, Dict, Optional
from datetime import datetime

app = FastAPI()
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "global": [],
            "logs": []
        }

    
    async def connect(self, ws: WebSocket):
        try:
            await ws.accept()
            self.active_connections["global"].append(ws)
            print(f"connections: {len(self.active_connections["global"])}")
        except Exception as e:
            logger.error(e)

    def disconnect(self, ws: WebSocket):
        self.active_connections["global"].remove(ws)
        self.active_connections["logs"].remove(ws)
        print(f"connections: {len(self.active_connections["global"])}")
    
    def add_to_logs_room(self, ws: WebSocket):
        self.active_connections["logs"].append(ws)

    async def send_logs(self, data: dict):
        jsonData = json.dumps(data)
        for connection in self.active_connections["logs"]:
            await connection.send_json(jsonData)

manager = ConnectionManager()

app.include_router(authRouter)
app.include_router(logRouter)
app.include_router(employeeRouter)
app.include_router(sessionRouter)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info(f"{websocket.client.host} got connected!")
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
                await manager.send_logs({
                    "method": "LOGS",
                    "data": {
                    "id": response.data,
                    "cookies": requestData["cookies"],
                    "headers": requestData["headers"],
                    "data": requestData["data"],
                    "method": requestData["method"],
                    "system_ip": requestData["system_ip"],
                    "url": requestData["url"],
                    "type": "Request",
                    "time": datetime.now().__str__()
                }
                })
                redisHelperInstance.addRecentRequest(system_ip=requestData["system_ip"], url=requestData["url"])
                print(response)

            elif(data["method"] == "ADD_RESPONSE"):
                responseData = data["data"]
                isRequestCached = redisHelperInstance.checkRecentRequest(system_ip=responseData["system_ip"], url=responseData["url"])
                if isRequestCached:
                    print("cache hit for response!")
                    response = dbHelperInstance.addResponse(cookies=responseData["cookies"], headers=responseData["headers"], data=responseData["data"], method=responseData["method"], system_ip=responseData["system_ip"], url=responseData["url"])
                    await manager.send_logs({
                        "method": "LOGS",
                        "data": {
                        "id": response.data,
                        "cookies": responseData["cookies"],
                        "headers": responseData["headers"],
                        "data": responseData["data"],
                        "method": responseData["method"],
                        "system_ip": responseData["system_ip"],
                        "url": responseData["url"],
                        "type": "Response",
                        "time": datetime.now().__str__()
                    }
                    })
                    print(response)

            elif(data["method"] == "GET_LOGS"):
                manager.add_to_logs_room(websocket)
            

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"{websocket.client.host} got disconnected!")


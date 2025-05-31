import json
from typing import Any

class CustomResponse:
    status: int
    success: bool
    data: dict
    message: str

    def __init__(self, status: int = 200, success: bool = True, data: Any = {}, message: str = "Done"):
        self.status = status
        self.data = data
        self.message = message
        self.success = success

    def toJson(self):
        return json.dumps({ "status": self.status, "success": self.success, "data": self.data, "message": self.message })
    
    def __str__(self):
        return self.toJson()

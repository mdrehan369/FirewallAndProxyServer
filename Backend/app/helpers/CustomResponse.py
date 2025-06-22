import json
from typing import Any

from fastapi.responses import JSONResponse


class CustomResponse:
    status: int
    success: bool
    data: dict
    message: str

    def __init__(
        self,
        status: int = 200,
        success: bool = True,
        data: Any = {},
        message: str = "Done",
    ):
        self.status = status
        self.data = data
        self.message = message
        self.success = success

    def toJson(self):
        return json.dumps(
            {
                "status": self.status,
                "success": self.success,
                "data": self.data,
                "message": self.message,
            }
        )

    def to_json_response(self):
        return JSONResponse(
            status_code=self.status,
            content={
                "status": self.status,
                "success": self.success,
                "data": self.data,
                "message": self.message,
            },
        )

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return self.toJson()

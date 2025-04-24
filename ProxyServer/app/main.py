from mitmproxy.http import HTTPFlow
from mitmproxy.connection import Client
from mitmproxy import http
from websockets.sync.client import connect
import json
import os
from utils.ad_patterns import ad_patterns
from utils.Logger import Logger
from utils.ActionMethod import ActionMethod
from dotenv import load_dotenv
from utils.errorHandler import errorHandler

load_dotenv()

class Server:

    db_helper = None
    redis_helper = None

    def __init__(self):
        self.num = 0
        self.logger = Logger()
        try:
            self.ws = connect(os.getenv("WEBSOCKET_SERVER"))
            self.logger.success("Websocket Connection Successfull!")
        except Exception as e:
            self.logger.error(f"Error while connecting with websocket server, {e}")

    @errorHandler
    def _sendWsMessage(self, actionMethod: ActionMethod, **data):
        message_dict = {
            "method": actionMethod.value,
            "data": {}
        }
        for k, v in data.items():
            message_dict["data"][k] = v

        self.ws.send(json.dumps(message_dict))

    # @errorHandler
    def request(self, flow: HTTPFlow):
        ua = flow.request.headers.get("User-Agent", "")
        accept = flow.request.headers.get("Accept", "")
        sec_fetch = flow.request.headers.get("Sec-Fetch-Site")

        if(any(p.match(flow.request.pretty_url) for p in ad_patterns)):
                    flow.response = http.Response.make(
                    200,
                    b"",
                    {"Content-Type": "text/plain"}  # Headers
                )
                    self.logger.info(f"Blocked ad request: {flow.request.pretty_url}")

        if "Mozilla" in ua and "text/html" in accept and sec_fetch:
            self._sendWsMessage(ActionMethod.CHECK_EMPLOYEE_STATUS, system_ip=flow.client_conn.address[0])
            data = self.ws.recv(10)
            isEmployeeLoggedIn = json.loads(data)

            if not isEmployeeLoggedIn["data"]["status"]:
                self.logger.info(f"Unauthorized Request Incoming: Redirecting To Login Page")
                flow.request.cookies.add("url", flow.request.pretty_url)
                flow.request.host = "localhost"
                flow.request.port = 8000
                flow.request.scheme = "http"
                flow.request.path = "/login"
                flow.request.cookies.add("system_ip", flow.client_conn.address[0])
                # flow.request.method = "GET"
            else:
                cookies = ""
                headers = ""

                for k, v in flow.request.cookies.items():
                    cookies += f"{k}:{v},"

                for k, v in flow.request.headers.items():
                    headers += f"{k}:{v},"


                self._sendWsMessage(ActionMethod.ADD_REQUEST, system_ip=flow.client_conn.address[0], cookies=cookies, headers=headers, url=flow.request.pretty_url, data=flow.request.text, method=flow.request.method)

    @errorHandler
    def response(self, flow: HTTPFlow):
        ua = flow.request.headers.get("User-Agent", "")
        accept = flow.request.headers.get("Accept", "")
        sec_fetch = flow.request.headers.get("Sec-Fetch-Site")

        if "Mozilla" in ua and "text/html" in accept and sec_fetch:
            cookies = ""
            headers = ""

            for k, v in flow.response.cookies.items():
                    cookies += f"{k}:{v},"

            for k, v in flow.response.headers.items():
                    headers += f"{k}:{v},"

            self._sendWsMessage(ActionMethod.ADD_RESPONSE, system_ip=flow.client_conn.address[0], cookies=cookies, headers=headers, url=flow.request.pretty_url, data=flow.request.text, method=flow.request.method)

addons=[Server()]
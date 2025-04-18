from mitmproxy.http import HTTPFlow
from mitmproxy.connection import Client
from mitmproxy import http
from websockets.sync.client import connect
import json
import os
from utils.ad_patterns import ad_patterns
from utils.Logger import Logger
from dotenv import load_dotenv

load_dotenv()


class Server:

    db_helper = None
    redis_helper = None

    def __init__(self):
        self.num = 0
        self.logger = Logger()
        self.logger.success("Logger Initialized Successfully!")
        try:
            self.ws = connect(os.getenv("WEBSOCKET_SERVER"))
            self.logger.success("Websocket Connection Successfull!")
        except Exception as e:
            self.logger.error(f"Error while connecting with websocket server, {e}")

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
            self.ws.send(json.dumps({ "method": "CHECK_EMPLOYEE_STATUS", "data": { "system_ip": flow.client_conn.address[0] } }))
            isEmployeeLoggedIn = json.loads(self.ws.recv(10))

            if not isEmployeeLoggedIn["data"]["status"]:
                self.logger.info(f"Unauthorized Request Incoming: Redirecting To Login Page")
                flow.request.cookies.add("url", flow.request.pretty_url)
                flow.request.host = "localhost"
                flow.request.port = 8000
                flow.request.scheme = "http"
                flow.request.path = "/login"
                flow.request.cookies.add("system_ip", flow.client_conn.address[0])

            
addons=[Server()]
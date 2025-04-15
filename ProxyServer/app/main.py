from mitmproxy.http import HTTPFlow
from mitmproxy.connection import Client
from mitmproxy import http
from termcolor import colored
from websockets.sync.client import connect
import json
import os

from dotenv import load_dotenv

load_dotenv()

class Logger:
    def __init__(self):
        print("Logger Initialized!")
    def print(self, text: str, color: str):
        print(colored(text, color))

class Server:

    db_helper = None
    redis_helper = None

    def __init__(self):
        self.num = 0
        self.logger = Logger()
        self.ws = connect(os.getenv("WEBSOCKET_SERVER"))

    def request(self, flow: HTTPFlow):
        ua = flow.request.headers.get("User-Agent", "")
        accept = flow.request.headers.get("Accept", "")
        sec_fetch = flow.request.headers.get("Sec-Fetch-Site")

        if "Mozilla" in ua and "text/html" in accept and sec_fetch:
            self.ws.send(json.dumps({ "method": "CHECK_EMPLOYEE_STATUS", "data": { "system_ip": flow.client_conn.address[0] } }))
            isEmployeeLoggedIn = json.loads(self.ws.recv(10))

            if not isEmployeeLoggedIn["data"]["status"]:
                flow.request.cookies.add("url", flow.request.url)
                flow.request.host = "localhost"
                flow.request.port = 8000
                flow.request.scheme = "http"
                flow.request.path = "/login"
                flow.request.cookies.add("system_ip", flow.client_conn.address[0])
            
addons=[Server()]
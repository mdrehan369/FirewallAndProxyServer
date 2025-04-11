from mitmproxy.http import HTTPFlow
from mitmproxy.connection import Client
from mitmproxy.proxy.server_hooks import ServerConnectionHookData
from mitmproxy import http
from termcolor import colored, COLORS
import os
from helpers.DbHelper import DbHelper
from helpers.RedisHelper import RedisHelper

# from .models import Attendance, Employee, IpTable, session

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
        self.db_helper = DbHelper()
        self.redis_helper = RedisHelper()
    
    def client_connected(self, client: Client):
        # print()
        # print(self.attendance)
        host = client.address[0]
        if self.redis_helper.checkSession(host) == False:
            pass
            # self.db_helper.
            # self.redis_helper.addSession(host, )
        # new_client = Attendance()

        # self.logger.print(f"A new client got connected with address {client.peername} and UUID ${client.id}", "green")
    
    def client_disconnected(self, client: Client):
        # print(self.attendance)
        print("disconnected")

        # self.logger.print(f"A client with address {client.peername} and UUID ${client.id} got disconnected!", "red")

    # def server_disconnected(self, data: ServerConnectionHookData):
    #     print(f"A server with address {data.server.peername} and UUID ${data.server.id} got disconnected!")
    
    # def server_connected(self, data: ServerConnectionHookData):
    #     print(f"A new server got connected with address {data.server.peername} and UUID ${data.server.id}")

    # def request(self, flow: HTTPFlow):
    #     # print("New request coming")
    #     if flow.request.pretty_url.find("img") == -1:
    #         print(f"{self.num}: {flow.timestamp_created}: {flow.client_conn.peername} {flow.request.method} {flow.request.pretty_url}\n")
    #         self.num += 1
    #     # print(flow.request.json())
    #     print(flow.request.pretty_host)
    
    def request(self, flow: HTTPFlow):
        ua = flow.request.headers.get("User-Agent", "")
        accept = flow.request.headers.get("Accept", "")
        sec_fetch = flow.request.headers.get("Sec-Fetch-Site")

        if "Mozilla" in ua and "text/html" in accept and sec_fetch:
            # print("Browser request detected")
            print("------------------------------------------------------------------------------------------")
            print("cookies", flow.request.cookies)
            print("data", flow.request.multipart_form)
            print("headers", flow.request.headers)
            print("pretty_url", flow.request.pretty_url)
            print("method", flow.request.method)
            print("timestamp_start", flow.request.timestamp_start)
            print("------------------------------------------------------------------------------------------")
            with open(os.path.join(os.getcwd(), "app/templates/Login.html"), "r") as f:
                html_content = f.read()
            flow.response = http.Response.make(
                200,
                html_content,
                {"Content-Type": "text/html"}
            )
        # else:
            # print("Likely a tool/script request")

    # def response(self, flow: HTTPFlow):
        # print("New response coming")
        # print(flow.response.json())

    # def responseheaders(self, flow: HTTPFlow):
    #     print("New response header coming")
    # # print(flow.response.json())

    # def requestheaders(self, flow: HTTPFlow):
    #     print("New request header coming")
    
    # def tcp_message(self, flow):
    #     print("A new TCp message")

    # def udp_message(self, flow):
    #     print("A new udp message")

addons=[Server()]

# with engine.connect() as conn:
#     userTable = Table("User", )
#     result = conn.execute(text("show tables"))
#     print(result.all())
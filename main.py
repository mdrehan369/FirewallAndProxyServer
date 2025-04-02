from mitmproxy.http import HTTPFlow
from mitmproxy.connection import Client
from mitmproxy.proxy.server_hooks import ServerConnectionHookData
from termcolor import colored, COLORS
import os

# from .models import Attendance, Employee, IpTable, session

class Logger:
    def __init__(self):
        pass
    def print(self, text: str, color: str):
        print(colored(text, color))

class Server:

    attendance = {}

    def __init__(self):
        self.num = 0
        self.logger = Logger()
    
    def client_connected(self, client: Client):
        # print()
        # print(self.attendance)
        host = client.address[0]
        # new_client = Attendance()
        if self.attendance.get(host) is None:
            self.logger.print(f"A new host {host} got connected!", "blue")
            self.attendance[f"{client.address[0]}"] = 1
            # isTodayFirstLogin = session.query().where(Attendance.login_at )
        else:
            self.attendance[f"{client.address[0]}"] += 1

        # self.logger.print(f"A new client got connected with address {client.peername} and UUID ${client.id}", "green")
    
    def client_disconnected(self, client: Client):
        # print(self.attendance)
        if(self.attendance.get(client.address[0]) == 1):
            self.logger.print(f"This host {client.address[0]} got disconnected!", "red")
            # self.attendance[client.address[0]]
            self.attendance.pop(client.address[0])
        else:
            self.attendance[f"{client.address[0]}"] -= 1

        # self.logger.print(f"A client with address {client.peername} and UUID ${client.id} got disconnected!", "red")

    # def server_disconnected(self, data: ServerConnectionHookData):
    #     print(f"A server with address {data.server.peername} and UUID ${data.server.id} got disconnected!")
    
    # def server_connected(self, data: ServerConnectionHookData):
    #     print(f"A new server got connected with address {data.server.peername} and UUID ${data.server.id}")

    def request(self, flow: HTTPFlow):
        # print("New request coming")
        if not flow.request.pretty_url.__contains__("img"):
            print(f"{self.num}: {flow.timestamp_created}: {flow.client_conn.peername} {flow.request.method} {flow.request.pretty_url}\n")
            self.num += 1
        # print(flow.request.json())

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
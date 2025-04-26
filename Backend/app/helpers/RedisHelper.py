from redis import Redis
from typing import Optional
import re
import json

ipv4_regex = r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'
url_regex = r'^(http:\/\/|https:\/\/)?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})(\/\S*)?$'

class RedisHelper():

    client = None

    def __init__(self, host: Optional[str] = "localhost", port: Optional[int] = 6379, password: Optional[str] = ""):
        self.client = Redis(host=host, port=port, password=password, decode_responses=True)
        response = self.client.ping()
        if response is None:
            print("Error in initializing Redis Client")
            return
        print("Redis Helper Initialized!")

    def addSession(self, host, session_id):
        self.client.set(host, session_id)

    def checkSession(self, host):
        if self.client.get(host) == None:
            return False
        else:
            return True
        
    def addRecentRequest(self, system_ip: str, url: str):
        """
            This function will add a cache of system IP with its URL with an expiry time of 5s
            and also it will create a cache of url with its response.
        """
        if not re.match(ipv4_regex, system_ip):
            return json.dumps({ "message": "Invalid system ip" })
        
        if not re.match(url_regex, url):
            return json.dumps({ "message": "Invalid URL" })
        
        self.client.set(system_ip, url)

        return json.dumps({ "message": "Done" })
    
    def checkRecentRequest(self, system_ip: str, url: str):
        url_cached = self.client.get(system_ip)
        if url_cached is None:
            return False
        if url_cached == url:
            self.client.delete(system_ip)
            return True
        return False
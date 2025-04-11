from redis import Redis

class RedisHelper():

    client = None

    def __init__(self):
        self.client = Redis()
        print("Redis Helper Initialized!")

    def addSession(self, host, session_id):
        self.client.set(host, session_id)

    def checkSession(self, host):
        if self.client.get(host) == None:
            return False
        else:
            return True
from redis import Redis

class RedisDB(object):
    connection = None

    def __init__(self):
        self.connection = Redis(host='localhost', port=6379, db=0)

    def get_connection(self):
        return self.connection


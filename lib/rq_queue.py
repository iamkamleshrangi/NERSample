from redis import Redis
from rq import Queue

def getConnections():
    q = Queue(connection=Redis())
    return q

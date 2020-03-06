import redis
from rq import Queue
import time

r = redis.Redis()
q = Queue(connection=r)


class Queue:
    @classmethod
    def add_queue(cls, fn, args):
        job = q.enqueue(fn, args)
        print("Hola")

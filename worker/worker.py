import os
from redis import Redis
from rq import Queue
from rq.worker import Worker

DB_REDIS = os.getenv('REDIS')
DB_REDIS_PORT = os.getenv('REDIS_PORT')

redis_url = f"redis://{DB_REDIS}:{DB_REDIS_PORT}/0"
redis = Redis.from_url(redis_url)

queue = Queue(connection=redis)
worker = Worker([queue], connection=redis)
worker.work()

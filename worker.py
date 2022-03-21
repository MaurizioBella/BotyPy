# -*- coding: utf-8 -*-
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from rq import Worker, Queue, Connection
import os
import redis

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

listen = ['high', 'default', 'low']

conn = redis.from_url(REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

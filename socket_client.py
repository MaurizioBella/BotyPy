# -*- coding: utf-8 -*-
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from backend.kw_extractor import run_kw_extractor
import redis
from rq import Queue
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logger
import os
from slack_bolt import App

load_dotenv()  # take environment variables from .env.
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

listen = ['high', 'default', 'low']

conn = redis.from_url(REDIS_URL)

q = Queue(connection=conn)

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("app_mention")
def handle_app_mention_events(body, client, logger, say):
    api_response = client.reactions_add(
        channel=body["event"]["channel"],
        timestamp=body["event"]["ts"],
        name="robot_face",
    )
    logger.debug(body)
    job = q.enqueue(run_kw_extractor, body, client)
    logger.debug('Job id: %s' % job.id)


@app.event("message")
def handle_message_events(body, client, say, logger):
    api_response = client.reactions_add(
        channel=body["event"]["channel"],
        timestamp=body["event"]["ts"],
        name="robot_face",
    )
    logger.debug(body)
    job = q.enqueue(run_kw_extractor, body, client)
    logger.debug('Job id: %s' % job.id)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

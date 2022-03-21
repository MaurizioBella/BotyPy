# -*- coding: utf-8 -*-
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from googleapiclient.discovery import build
import os
import logger
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
GOOGLE_SEARCH_API_KEY = REDIS_URL = os.getenv(
    'GOOGLE_SEARCH_API_KEY')
GOOGLE_CSE_ID = os.getenv(
    'GOOGLE_CSE_ID')


def search_google(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=GOOGLE_SEARCH_API_KEY)
    res = service.cse().list(q=search_term, cx=GOOGLE_CSE_ID, **kwargs).execute()
    text = ""
    for i in res['items'][0:3]:
        # print(i['title'])
        text = "".join(
            [text, f"<{i['link']}|{i['title']}>\n>{i['snippet']}\n>\n"])
    return text


def search(search_term, **kwargs):
    if GOOGLE_SEARCH_API_KEY is not None:
        logger.config().debug('Using google search')
        return search_google(search_term, **kwargs)

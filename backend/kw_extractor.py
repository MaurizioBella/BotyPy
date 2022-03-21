# -*- coding: utf-8 -*-
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import re
import os
import logger
from backend.kw_search import search
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
KW_EXTRACTOR_KEYBERT_TOPN = os.getenv("KW_EXTRACTOR_KEYBERT_TOPN", 1)
KW_EXTRACTOR_KEYBERT_RANGE = os.getenv("KW_EXTRACTOR_KEYBERT_RANGE", 3)


def kw_extractor_keybert(doc):
    from keybert import KeyBERT
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(doc)
    result = kw_model.extract_keywords(doc, keyphrase_ngram_range=(int(KW_EXTRACTOR_KEYBERT_RANGE), int(KW_EXTRACTOR_KEYBERT_RANGE)), stop_words='english',
                                       use_mmr=True, diversity=0.7, top_n=int(KW_EXTRACTOR_KEYBERT_TOPN))
    listToStr = ' '.join([str(elem) for elem, key in result])
    return listToStr


def run_kw_extractor(body, client):
    text = body["event"]["text"]
    text = re.sub(r"<\@\w+>", "", text)
    key_words = kw_extractor_keybert(text)
    text = f"Here what I found for keys words: \"_{key_words}_\"\n"
    sites_found = search(key_words)
    if sites_found is not None:
        text = "".join([text, sites_found])
    logger.config().debug(text)
    client.chat_postMessage(
        channel=body["event"]["channel"],
        thread_ts=body["event"]["ts"],
        text=text,
    )

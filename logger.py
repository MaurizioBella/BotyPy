# -*- coding: utf-8 -*-
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os
import logging
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'ERROR')


def config():
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(filename)s (%(lineno)s): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    return logger


if __name__ == "logger":
    config()

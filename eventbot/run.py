#!/usr/bin/env python

import logging
import pprint

from app import app

import settings

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(format=settings.LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

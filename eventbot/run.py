#!/usr/bin/env python

import logging

from app import app

import settings

logging.basicConfig(format=settings.LOG_FORMAT, level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

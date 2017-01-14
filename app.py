#!/usr/bin/env python

from flask import Flask

import flask
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/webhook/application_form", methods=['POST', 'GET'])
def web_hook_application_form():
    logger.info("web_hook_application_form")
    d = {
        'status': 'ok'
    }
    return flask.jsonify(**d)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

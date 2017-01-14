#!/usr/bin/env python

from flask import Flask

import flask
import logging
import simplejson as json

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
        'status': 'ok',
        'body': flask.request.data
    }
    # logger.info(flask.request.data)
    logger.info("request data: {}".format(flask.request.data))
    logger.info("request form: {}".format(flask.request.form))
    logger.info("request headers: {}".format(flask.request.headers))
    logger.info("d: {}".format(json.dumps(d)))
    return flask.jsonify(**d)
    # return flask.jsonify(**flask.request.get_json())
    # return flask.request.get_json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

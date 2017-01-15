#!/usr/bin/env python

from flask import Flask

from forms import ApplicationForm
import flask
import logging
import simplejson as json
from integrations import slack

app = Flask(__name__)

app.config.setdefault('WTF_CSRF_ENABLED', False)
LOG_FORMAT = '[%(asctime)s] %(filename)s:%(lineno)s - %(funcName)20s() [%(levelname)s] %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def hello():
    d = {'status': 'ok'}
    return flask.jsonify(**d)


@app.route("/webhook/application_form", methods=['POST', 'GET'])
def web_hook_application_form():
    """ Web hook for incoming application forms.
    """
    logger.info("Received form: {}".format(flask.request.form))
    form = ApplicationForm()
    logger.debug("request headers: {}".format(flask.request.headers))
    d = {
        'status': 'ok',
        'form': flask.request.form
    }
    if form.validate_on_submit():
        slack.post_form_to_webhook(form)
    logger.debug("d: {}".format(json.dumps(d)))
    return flask.jsonify(**d)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#!/usr/bin/env python

from flask import Flask
from forms import ApplicationForm
from integrations import slack, eventbrite_client
import flask
import logging
import pprint
import settings
import simplejson as json

app = Flask(__name__)

app.config.setdefault('WTF_CSRF_ENABLED', False)
pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(format=settings.LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

HTTP_HEADER_REQUEST_ID = 'X-Request-ID'


@app.route("/")
def hello():
    d = {'status': 'ok'}
    return flask.jsonify(**d)


@app.route("/webhook/application_form", methods=['POST', 'GET'])
def web_hook_application_form():
    """ Web hook for incoming application forms.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    logger.info(u"request_id={} Received form: {}".format(request_id, flask.request.form))
    form = ApplicationForm()
    logger.debug("request_id={} request headers: {}".format(request_id, flask.request.headers))
    d = {
        'status': 'ok',
        'form': flask.request.form
    }
    if form.validate_on_submit():
        slack.post_form_to_webhook(form)
    logger.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return flask.jsonify(**d)


@app.route("/webhook/eventbrite", methods=['POST', 'GET'])
def web_hook_eventbrite():
    """ Web hook for incoming Eventbrite changes.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    # logger.info(u"request_id={} Received Eventbrite notification: {}".format(request_id, flask.request.form))
    request_data = flask.request.get_json()
    logger.info("request_id={} headers={} body={}".format(request_id, flask.request.headers, json.dumps(request_data)))
    logger.info('request_data:{}'.format(json.dumps(request_data)))
    if request_data['config']['action'] == 'order.placed':
        logger.info("Order placed!")
    d = {
        'status': 'ok',
        'data': request_data
    }
    # pp.pprint(request_data)
    logger.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return flask.jsonify(**d)


@app.route("/webhook/mailchimp", methods=['POST', 'GET'])
def web_hook_mailchimp():
    """ Web hook for incoming MailChimp changes.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    request_data = flask.request.get_json()
    # logger.info(u"request_id={} Received MailChimp notification: {}".format(request_id, flask.request.form))
    logger.info("request_id={} headers={} body={}".format(request_id, flask.request.headers, json.dumps(request_data)))
    d = {
        'status': 'ok',
        'data': request_data
    }
    logger.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return flask.jsonify(**d)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#!/usr/bin/env python

from flask import Flask, request
from forms import ApplicationForm
from integrations import slack, eventbrite_client, mailchimp_client
from integrations.mailchimp_client import NotFoundException
import flask
import logging
import pprint
import requests
import settings
import simplejson as json

app = Flask(__name__)

app.config.setdefault('WTF_CSRF_ENABLED', False)
pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(format=settings.LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)

HTTP_HEADER_REQUEST_ID = 'X-Request-ID'


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def hello():
    d = {'status': 'ok'}
    return flask.jsonify(**d)


@app.route("/command", methods=['POST'])
def command():
    """ Verify a working connection.
    """
    return "Your ngrok tunnel is up and running!"


@app.route("/oauth", methods=['GET'])
def oauth():
    """ Verify an OAuth request.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    log.info("request_id='{}'".format(request_id))
    log.info("headers='{}'".format(str(request.headers).replace('\r\n', ',')))
    log.info("query_string='{}'".format(request.query_string))
    code = flask.request.args.get('code')
    if not code:
        log.error("No code specified")
        raise InvalidUsage('No OAuth code specified!')
    else:
        log.info("code={}".format(code))
        url = "https://slack.com/api/oauth.access"
        payload = {
            "code": code,
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET
        }
        resp = requests.get(url, params=payload)
        return flask.jsonify(**resp.json())


@app.route("/slack/action-endpoint", methods=['POST', 'GET'])
def web_hook_slack_action_endpoint():
    """ Receives requests from Slack when someone presses a button in an interactive message.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    request_data = flask.request.get_json()
    # logger.info(u"request_id={} Received MailChimp notification: {}".format(request_id, flask.request.form))
    log.info("request_id={} headers={} body={}".format(request_id, flask.request.headers, json.dumps(request_data)))
    d = {
        'status': 'ok',
        'data': request_data
    }
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return flask.jsonify(**d)


@app.route("/webhook/application_form", methods=['POST', 'GET'])
def web_hook_application_form():
    """ Web hook for incoming application forms.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    log.info(u"request_id={} Received form: {}".format(request_id, flask.request.form))
    form = ApplicationForm()
    log.debug("request_id={} request headers: {}".format(request_id, flask.request.headers))
    d = {
        'status': 'ok',
        'form': flask.request.form
    }
    if form.validate_on_submit():
        slack.post_form_to_webhook(form)
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return flask.jsonify(**d)


def check_interests(email, interests):
    """ Check an Eventbrite attendee against a set of interests (groups) in MailChimp.
    """
    mc = mailchimp_client.MailChimpClient(api_key=settings.MAILCHIMP_APIKEY)
    o = {}
    for interest in interests:
        has_interest = mc.check_interest(
            email,
            settings.MAILCHIMP_DEFAULT_LIST,
            settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
            interest
        )
        o[interest] = has_interest
    return o


def check_membership(eb_attendee_url):
    """ Check membership status of an event attendee.
    """
    log.info("Checking membership for url={}".format(eb_attendee_url))
    eb = eventbrite_client.EventbriteClient(settings.EVENTBRITE_OAUTH_TOKEN)
    attendee = eb.get_url(eb_attendee_url)
    log.info('attendee: {}'.format(json.dumps(attendee)))
    email = attendee['profile']['email']
    try:
        check_interests(email, ["Socialites", "Members"])
    except NotFoundException as e:
        log.warn(e.message)
        slack.post_warning_to_webhook("{} just bought a ticket for an event but is not in our database!".format(email))
    event_id = attendee['event_id']


@app.route("/webhook/eventbrite", methods=['POST', 'GET'])
def web_hook_eventbrite():
    """ Web hook for incoming Eventbrite changes.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    # logger.info(u"request_id={} Received Eventbrite notification: {}".format(request_id, flask.request.form))
    request_data = flask.request.get_json()
    log.info("request_id={} headers={} body={}".format(request_id, flask.request.headers, json.dumps(request_data)))
    log.info('request_data:{}'.format(json.dumps(request_data)))
    if request_data['config']['action'] == 'attendee.updated':
        log.info("Order placed!")
        check_membership(request_data['api_url'])
    d = {
        'status': 'ok',
        'data': request_data
    }
    # pp.pprint(request_data)
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return flask.jsonify(**d)


@app.route("/webhook/mailchimp", methods=['POST', 'GET'])
def web_hook_mailchimp():
    """ Web hook for incoming MailChimp changes.
    """
    request_id = flask.request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    request_data = flask.request.get_json()
    # logger.info(u"request_id={} Received MailChimp notification: {}".format(request_id, flask.request.form))
    log.info("request_id={} headers={} body={}".format(request_id, flask.request.headers, json.dumps(request_data)))
    d = {
        'status': 'ok',
        'data': request_data
    }
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return flask.jsonify(**d)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

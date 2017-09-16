import logging
import pprint
import requests
import simplejson as json
from flask import jsonify, request
from . import app
import eventbot.settings
import urllib
# from attendee_reporter import check_membership
from errors import InvalidUsage
from slack import api_client as slack
from slack import action as slack_action
from forms import ApplicationForm

HTTP_HEADER_REQUEST_ID = 'X-Request-ID'

log = logging.getLogger(__name__)

pp = pprint.PrettyPrinter(indent=4)

ROUTES_WEB_HOOK_SLACK_SLASH_COMMAND_ATTENDEES = '/webhook/slack/command/attendees'


def log_request():
    """ Log request details.
    """
    request_id = request.headers.get(HTTP_HEADER_REQUEST_ID, 'unknown')
    log.debug(u"request_id='{}'".format(request_id))
    log.debug(u"headers='{}'".format(str(request.headers).replace('\r\n', ',')))
    log.debug(u"query_string='{}'".format(request.query_string))
    log.debug(u"body='{}'".format(request.get_data().decode('utf-8')))
    return request_id


@app.route("/")
def hello():
    d = {'status': 'ok'}
    return jsonify(**d)


@app.route("/command", methods=['POST'])
def command():
    """ Verify a working connection.
    """
    return "Your ngrok tunnel is up and running!"


@app.route("/action", methods=['POST'])
def action():
    """ Processes actions from interactive message button presses.
    """
    log_request()
    pass


@app.route("/oauth", methods=['GET'])
def oauth():
    """ Verify an OAuth request.
    """
    log_request()
    code = request.args.get('code')
    if not code:
        log.error("No code specified")
        raise InvalidUsage('No OAuth code specified!')
    else:
        log.info("code={}".format(code))
        url = "https://slack.com/api/oauth.access"
        payload = {
            "code": code,
            "client_id": eventbot.settings.SLACK_CLIENT_ID,
            "client_secret": eventbot.settings.SLACK_CLIENT_SECRET
        }
        resp = requests.get(url, params=payload)
        return jsonify(**resp.json())


@app.route(ROUTES_WEB_HOOK_SLACK_SLASH_COMMAND_ATTENDEES, methods=['POST'])
def web_hook_slack_slash_command_attendees():
    """ For processing '/attendees' commands.
    """
    request_id = log_request()
    data = request.get_data().decode('utf-8')
    log.info("web_hook_slack_slash_command_attendees")
    return "ok {}".format(request_id)


@app.route("/slack/action-endpoint", methods=['POST', 'GET'])
def web_hook_slack_action_endpoint():
    """ Receives requests from Slack when someone presses a button in an interactive message.
    """
    request_id = log_request()
    data = request.get_data().decode('utf-8')
    resp = slack_action.parse_post(data)
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(data)))
    user = resp['payload']['user']['name']
    email = resp['payload']['callback_id']
    original_message_text = resp['payload']['original_message']['text']
    log.info(u"{} successfully approved {}".format(user, email))
    message = u"""
{}

*Successful approval by {}.*
""".format(
        urllib.unquote_plus(original_message_text),
        user
    )
    return message


@app.route("/webhook/application_form", methods=['POST', 'GET'])
def web_hook_application_form():
    """ Web hook for incoming application forms.
    """
    request_id = log_request()
    log.info(u"request_id={} Received form: {}".format(request_id, request.form))
    data = request.form.to_dict()
    log.debug(u"request_id={} Data: {}".format(request_id, data))
    form = ApplicationForm(data=data)
    d = {
        'status': 'ok',
        'form': request.form,
        'data': data,
    }
    slack.post_form_to_webhook(form)
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return jsonify(**d)


@app.route("/webhook/eventbrite", methods=['POST', 'GET'])
def web_hook_eventbrite():
    """ Web hook for incoming Eventbrite changes.
    """
    request_id = log_request()
    request_data = request.get_json()
    # if request_data['config']['action'] == 'attendee.updated':
    #     log.info("Order placed!")
    #     check_membership(request_data['api_url'])
    d = {
        'status': 'ok',
        'data': request_data
    }
    # pp.pprint(request_data)
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return jsonify(**d)


@app.route("/webhook/mailchimp", methods=['POST', 'GET'])
def web_hook_mailchimp():
    """ Web hook for incoming MailChimp changes.
    """
    request_id = log_request()
    request_data = request.get_json()
    d = {
        'status': 'ok',
        'data': request_data
    }
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return jsonify(**d)


@app.route("/webhook/typeform", methods=['POST', 'GET'])
def web_hook_typeform():
    """ Web hook for incoming Typeform changes.
    """
    request_id = log_request()
    request_data = request.get_json()
    d = {
        'status': 'ok',
        'data': request_data
    }
    log.debug(u"request_id={} d: {}".format(request_id, json.dumps(d)))
    return jsonify(**d)

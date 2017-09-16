# coding=utf-8

from eventbot import settings
from eventbot.app.mailchimp.api_client import MailChimpClient, MailChimpInterestManager
from eventbot.app.eventbrite.api_client import EventbriteClient
import logging
import pprint
import simplejson as json
import urllib

log = logging.getLogger(__name__)


pp = pprint.PrettyPrinter(indent=4)


# TODO Make it exclude refunded tickets and other 'not attending' people.
# TODO Dynamically select the event ID based on date.
def parse_attendees_command(user_name):
    """
    Returns a list of attendees, sorted by ticket class.
    :param user_name:
    :return:
    """
    eb_client = EventbriteClient(settings.EVENTBRITE_OAUTH_TOKEN)
    event_id = '37330486490'
    attendee_data = eb_client.get_event_attendees(event_id)
    log.debug(attendee_data[0])
    attendee_data_by_ticket_type = sorted(attendee_data, key=lambda k: k['ticket_class_name'])
    lines = [
        '{}\t{}\t{}\t{}'.format(
            i+1,
            x['ticket_class_name'].ljust(20),
            x['profile']['name'].ljust(30),
            x['profile']['email']
        ) for i, x in enumerate(attendee_data_by_ticket_type)
    ]
    slack_message = 'Attendee list for {}: \n{}'.format(user_name, '\n'.join(lines))
    return slack_message


def parse_slash_command(command, user_name, request_data):
    """
    Process a slash command message from Slack.
    :param command: the name of the command
    :type command: basestring
    :param user_name: the user name of the Slack user who initiated the command
    :type user_name: basestring
    :param request_data: the entire request_data from Flask as an Im
    :type request_data: ImmutableDict
    :return: basestring
    """
    log.debug(u"Request data: {}".format(json.dumps(request_data)))
    if command[1:] == 'attendees':
        message = parse_attendees_command(user_name)
    return message

def parse_post(body):
    """ Parse a POST request from Slack.
    """
    payload = json.loads(urllib.unquote(body.split('=')[1]))
    log.debug(u"Payload: {}".format(json.dumps(payload)))
    resp = _approve_socialite(email_address=payload['callback_id'])
    obj = {
        'payload': payload,
        'unencoded_payload': payload,
        'mailchimp_response': resp
    }
    return obj


def _approve_socialite(email_address):
    """ Approve a socialite.
    """
    manager = MailChimpInterestManager(
        MailChimpClient(settings.MAILCHIMP_APIKEY),
        settings.MAILCHIMP_DEFAULT_LIST,
        settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY
    )
    member = manager.get_member(email_address=email_address)
    resp = manager.add_interest(member['id'], settings.MAILCHIMP_INTEREST_NAME_SOCIALITE)
    return resp

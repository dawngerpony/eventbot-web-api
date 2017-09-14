# coding=utf-8

from eventbot import settings
from eventbot.app.mailchimp.api_client import MailChimpClient, MailChimpInterestManager
import logging
import pprint
import simplejson as json
import urllib

log = logging.getLogger(__name__)


pp = pprint.PrettyPrinter(indent=4)


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

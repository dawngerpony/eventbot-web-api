# coding=utf-8

from eventbot import settings
import eventbot.app.mailchimp.api_client
import hashlib
import logging
import pprint
import simplejson as json
import sys
import urllib

log = logging.getLogger(__name__)


pp = pprint.PrettyPrinter(indent=4)


def parse_post(body):
    """ Parse a POST request from Slack.
    """
    mc = eventbot.app.mailchimp.api_client.MailChimpClient(settings.MAILCHIMP_APIKEY)
    payload = json.loads(urllib.unquote(body.split('=')[1]))
    log.debug(u"Payload: {}".format(json.dumps(payload)))
    callback_id = payload['callback_id']
    m = hashlib.md5()
    m.update(callback_id.lower())
    subscriber_hash = m.hexdigest()
    list_id = mc.lookup_list_id(settings.MAILCHIMP_DEFAULT_LIST)
    member = mc.get_member(subscriber_hash, list_id)
    member['interests'][settings.MAILCHIMP_INTEREST_ID_SOCIALITE] = True
    resp = mc.update_member(subscriber_hash, list_id, member)
    obj = {
        'payload': payload,
        'unencoded_payload': payload,
        'mailchimp_response': resp
    }
    return obj

from eventbot import settings
import eventbot.app.mailchimp.api_client
import hashlib
import logging
import pprint
import simplejson as json
import urllib

log = logging.getLogger(__name__)


pp = pprint.PrettyPrinter(indent=4)


def parse_post(body):
    """ Parse a POST request from Slack.
    """
    mc = eventbot.app.mailchimp.api_client.MailChimpClient(settings.MAILCHIMP_APIKEY)
    payload = json.loads(urllib.unquote(body.split('=')[1]))
    log.debug(u"Payload: {}".format(json.dumps(payload, indent=2)))
    callback_id = payload['callback_id']
    log.info(u"callback_id={}".format(callback_id))
    m = hashlib.md5()
    m.update(callback_id.lower())
    subscriber_hash = m.hexdigest()
    log.info(u"subscriber_hash={}".format(subscriber_hash))
    list_id = mc.lookup_list_id(settings.MAILCHIMP_DEFAULT_LIST)
    member = mc.get_member(subscriber_hash, list_id)
    log.debug(member)
    log.debug(member['interests'])
    member['interests'][settings.MAILCHIMP_INTEREST_ID_SOCIALITE] = True
    resp = mc.update_member(subscriber_hash, list_id, member)
    obj = {
        'payload': payload,
        'resp': resp
    }
    return obj

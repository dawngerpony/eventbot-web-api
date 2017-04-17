import logging
import requests
import simplejson as json

from eventbot import settings

log = logging.getLogger(__name__)


def post_form_to_webhook(form):
    """ Post the contents of a form to Slack.
    """
    d = form.values()
    log.debug("d: {}".format(d))
    text = u"""
    '{name}' ({email}) submitted an application form.
    *Please tell us about yourself:* {bio}
    *What interests you?* {interests}
    """.format(**d)

    slack_webhook_obj = {
        "text": text,
        "attachments": [
            {
                "fallback": "Required plain-text summary of the attachment.",
                "color": "#36a64f",
                "title": "Image 1",
                "image_url": d.get('imageUrl', 'https://placehold.it/150x150?text=unknown'),
            },
            {
                "text": "What action should I take?",
                "fallback": "No action chosen",
                "callback_id": d['email'],
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "application_form",
                        "text": "Approve",
                        "type": "button",
                        "value": "approve"
                    }
                ]
            }
        ]
    }
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    requests.post(slack_webhook_url, data=json.dumps(slack_webhook_obj))


def post_warning_to_webhook(message):
    """ Post a warning into Slack.
    """
    text = u"""
    Warning! {message}
    """.format(**message)
    slack_webhook_obj = {"text": text}
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    requests.post(slack_webhook_url, data=json.dumps(slack_webhook_obj))

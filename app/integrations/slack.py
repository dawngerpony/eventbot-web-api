import requests
import simplejson as json

from app import settings


def post_form_to_webhook(form):
    """ Post the contents of a form to Slack.
    """
    d = form.values()
    text = """
    '{name}' ({email}) submitted an application form.
    *Please tell us about yourself:* {bio}
    *What interests you?* {interests}
    """.format(**d)

    slack_webhook_obj = {"text": text}
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    requests.post(slack_webhook_url, data=json.dumps(slack_webhook_obj))

import requests
import simplejson as json

BASE_URL = 'http://localhost:5000'

HEADERS = {
    'Content-Type': 'application/json'
}


def test_webhook_application_form():
    """ Test the webhook application form.
    """
    body = {
        'foo': 'bar'
    }
    r = requests.post('{}/webhook/application_form'.format(BASE_URL), json.dumps(body), headers=HEADERS)
    o = r.json()
    print o
    assert o['status'] == 'ok', o['status']

import requests

BASE_URL = 'http://localhost:5000'


def test_webhook_application_form():
    """ Test the webhook application form.
    """
    expected_name = 'Dafydd Integration Test'
    expected_email = 'dafydd@afterpandora.com'
    expected_bio = 'bio'
    expected_interests = 'interests'
    payload = {
        'Field3': expected_name,
        'Field5': expected_email,
        'Field11': expected_bio,
        'Field12': expected_interests
    }
    r = requests.post('{}/webhook/application_form'.format(BASE_URL), data=payload)
    o = r.json()
    # print json.dumps(o, indent=2)
    assert o['status'] == 'ok', o['status']
    # assert o['Field3']['data'] == expected_name, o['Field3']['data']

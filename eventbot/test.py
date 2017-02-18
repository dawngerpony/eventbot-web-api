# coding=utf-8
import bot
import simplejson as json
import unittest


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = bot.app.test_client()

    def tearDown(self):
        pass

    def test_webhook_application_form(self):
        rv = self.app.post('/webhook/application_form', data=build_form_payload())
        o = json.loads(rv.data)
        assert o['status'] == 'ok', o['status']

    def test_webhook_eventbrite(self):
        data = {}
        rv = self.app.post('/webhook/eventbrite', data=data)
        o = json.loads(rv.data)
        assert o['status'] == 'ok', o['status']


def build_form_payload():
    """ Build a payload for the test.
    """
    expected_name = u'Dafydd Integråtion Tëst'
    expected_email = 'dafydd@afterpandora.com'
    expected_bio = 'bio'
    expected_interests = 'interests'
    payload = {
        'Field3': expected_name,
        'Field5': expected_email,
        'Field11': expected_bio,
        'Field12': expected_interests
    }
    return payload

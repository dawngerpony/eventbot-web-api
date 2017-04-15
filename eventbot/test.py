# coding=utf-8
from app import app
from simplejson import JSONDecodeError
import simplejson as json
import test_fixtures as fixtures
import unittest


class ApiTestCase(unittest.TestCase):

    app = None

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_webhook_application_form(self):
        self.post_json_to_webhook(path='/webhook/application_form', data=build_form_payload())

    # @unittest.skip("testing skipping")
    def test_webhook_eventbrite(self):
        data = {'test': True}
        o = self.post_json_to_webhook(path='/webhook/mailchimp', data=data)
        assert o['data']['test'] is True, o

    # @unittest.skip("testing skipping")
    def test_webhook_eventbrite_order_placed(self):
        o = self.post_json_to_webhook(
            path='/webhook/mailchimp',
            data=json.loads(fixtures.EVENTBRITE_ORDER_PLACED)
        )
        assert o['data']['config']['action'] == 'order.placed', o

    # @unittest.skip("testing skipping")
    def test_webhook_mailchimp(self):
        data = {
            'test': True
        }
        o = self.post_json_to_webhook(path='/webhook/mailchimp', data=data)
        assert o['data']['test'] is True, o

    def post_json_to_webhook(self, path, data):
        resp = self.app.post(path, data=json.dumps(data), content_type='application/json')
        try:
            o = json.loads(resp.data)
        except JSONDecodeError as e:
            print resp.data
        assert o['status'] == 'ok', o['status']
        return o


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

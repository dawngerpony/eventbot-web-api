# coding=utf-8
from app import app
from simplejson import JSONDecodeError
import logging
import settings
import simplejson as json
import test_fixtures as fixtures
import unittest
import urllib

logging.basicConfig(format=settings.LOG_FORMAT, level=logging.DEBUG)


class ApiTestCase(unittest.TestCase):

    app = None

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    # @unittest.SkipTest
    def test_webhook_application_form(self):
        self.post_form_to_webhook(path='/webhook/application_form', data=build_form_payload())

    # @unittest.SkipTest
    def test_webhook_eventbrite(self):
        data = {'test': True}
        o = self.post_to_endpoint(path='/webhook/eventbrite', data=data)
        assert o['data']['test'] is True, o

    # @unittest.SkipTest
    def test_webhook_eventbrite_order_placed(self):
        o = self.post_to_endpoint(
            path='/webhook/eventbrite',
            data=json.loads(fixtures.EVENTBRITE_ORDER_PLACED)
        )
        assert o['data']['config']['action'] == 'order.placed', o

    # @unittest.SkipTest
    def test_webhook_mailchimp(self):
        data = {
            'test': True
        }
        o = self.post_to_endpoint(path='/webhook/mailchimp', data=data)
        assert o['data']['test'] is True, o

    # @unittest.SkipTest
    def test_webhook_typeform(self):
        data = {
            'test': True
        }
        o = self.post_to_endpoint(path='/webhook/typeform', data=data)
        assert o['data']['test'] is True, o

    def test_slack_action_endpoint(self):
        data = fixtures.SLACK_ACTION_ENDPOINT_EXAMPLE_1
        email = urllib.quote(settings.MAILCHIMP_DEFAULT_EMAIL)
        data = data.replace('application_form_action', email)
        o = self.post_to_endpoint(path='/slack/action-endpoint', data=data, is_json_data=False, is_json_response=False)
        assert "Successful approval" in o

    def post_to_endpoint(self, path, data, is_json_data=True, is_json_response=True):
        if is_json_data:
            resp = self.app.post(path, data=json.dumps(data), content_type='application/json')
        else:
            resp = self.app.post(path, data=data)
        if is_json_response:
            try:
                o = json.loads(resp.data)
            except JSONDecodeError as e:
                print resp.data
                self.fail("Problem decoding JSON")
            assert o['status'] == 'ok', o['status']
            return o
        else:
            return resp.data

    def post_form_to_webhook(self, path, data):
        resp = self.app.post(path, data=data)
        try:
            o = json.loads(resp.data)
        except JSONDecodeError:
            print resp.data
            self.fail("Problem decoding JSON")
        assert o['status'] == 'ok', o['status']
        return o


def build_form_payload():
    """ Build a payload for the test.
    """
    expected_name = u'Dafydd Integråtion Tëst'
    expected_email = settings.MAILCHIMP_DEFAULT_EMAIL
    expected_bio = 'bio'
    expected_interests = 'interests'
    expected_image_url = 'https://placehold.it/350x150?text=woohoo'
    payload = {
        'Field3': expected_name,
        'Field5': expected_email,
        'Field11': expected_bio,
        'Field12': expected_interests,
        'Field17-url': expected_image_url
    }
    return payload

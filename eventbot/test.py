# coding=utf-8
from __future__ import print_function
from app import app, routes, mailchimp
from simplejson import JSONDecodeError
import logging
import mock_objects as mocks
import requests_mock
import settings
import simplejson as json
import test_fixtures as fixtures
import unittest
import urllib

logging.basicConfig(format=settings.LOG_FORMAT, level=logging.DEBUG)

settings.USE_CACHE = False


@requests_mock.Mocker()
class ApiTestCase(unittest.TestCase):

    app = None

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    # @unittest.SkipTest
    def test_webhook_application_form_success(self, m):
        m.register_uri('POST', url=settings.SLACK_WEBHOOK_URL, text='foo')
        self.post_form_to_webhook(path=routes.ROUTES_WEB_HOOK_APPLICATION_FORM, data=build_form_payload())

    # @unittest.SkipTest
    def test_webhook_eventbrite_success(self, m):
        data = {'test': True}
        o = self.post_to_endpoint(path=routes.ROUTES_WEB_HOOK_EVENTBRITE, data=data)
        assert o['data']['test'] is True, o

    # @unittest.SkipTest
    def test_webhook_eventbrite_order_placed_success(self, m):
        o = self.post_to_endpoint(
            path='/webhook/eventbrite',
            data=json.loads(fixtures.EVENTBRITE_ORDER_PLACED)
        )
        assert o['data']['config']['action'] == 'order.placed', o

    # @unittest.SkipTest
    def test_webhook_mailchimp_success(self, m):
        data = {
            'test': True
        }
        o = self.post_to_endpoint(path='/webhook/mailchimp', data=data)
        assert o['data']['test'] is True, o

    # @unittest.SkipTest
    def test_webhook_typeform_success(self, m):
        data = {
            'test': True
        }
        o = self.post_to_endpoint(path='/webhook/typeform', data=data)
        assert o['data']['test'] is True, o

    # @unittest.SkipTest
    def test_slack_action_endpoint_success(self, m):
        email = urllib.quote(settings.MAILCHIMP_DEFAULT_EMAIL)
        lists_base_url = '{}/lists'.format(mailchimp.api_client.BASE_URL)
        subscriber_hash = mailchimp.api_client.calculate_subscriber_hash(settings.MAILCHIMP_DEFAULT_EMAIL)
        m.register_uri('GET', url=lists_base_url, json=mocks.MAILCHIMP_MOCK_RESPONSE_LISTS)
        m.register_uri(
            'GET',
            url='{}/False/interest-categories'.format(lists_base_url),
            json=mocks.MAILCHIMP_MOCK_RESPONSE_INTEREST_CATEGORIES
        )
        m.register_uri(
            'GET',
            url='{}/False/members/{}'.format(lists_base_url, subscriber_hash),
            json=mocks.MAILCHIMP_MOCK_RESPONSE_MEMBER
        )
        m.register_uri(
            'GET',
            url='{}/False/members/foo'.format(lists_base_url),
            json=mocks.MAILCHIMP_MOCK_RESPONSE_MEMBER
        )
        m.register_uri(
            'GET',
            url='{}/False/interest-categories/foo/interests'.format(lists_base_url, subscriber_hash),
            json=mocks.MAILCHIMP_MOCK_RESPONSE_INTERESTS
        )
        m.register_uri(
            'PATCH',
            url='{}/False/members/foo'.format(lists_base_url),
            text='{"status": "ok"}'
        )
        m.register_uri(
            'GET',
            url='{}/False/members/{}'.format(lists_base_url, subscriber_hash),
            json=mocks.MAILCHIMP_MOCK_RESPONSE_MEMBER
        )
        data = fixtures.SLACK_ACTION_ENDPOINT_EXAMPLE_1
        data = data.replace('application_form_action', email)
        o = self.post_to_endpoint(path='/slack/action-endpoint', data=data, is_json_data=False, is_json_response=False)
        assert "Successful approval" in o

    # @unittest.SkipTest
    def test_web_hook_slack_slash_command_attendees_success(self, m):
        m.register_uri(
            'GET',
            url='https://www.eventbriteapi.com/v3/events/q/attendees/',
            json=mocks.EVENTBRITE_MOCK_RESPONSE_ATTENDEES
        )
        data = fixtures.ROUTES_WEB_HOOK_SLACK_SLASH_COMMAND_ATTENDEES_EXAMPLE_1
        path = routes.ROUTES_WEB_HOOK_SLACK_SLASH_COMMAND_ATTENDEES
        o = self.post_to_endpoint(
            path=path,
            data=data,
            is_json_data=False,
            is_json_response=False
        )
        self.assertIn('Attendee list for {}'.format(data['user_name']), o)

    def post_to_endpoint(self, path, data, is_json_data=True, is_json_response=True):
        if is_json_data:
            resp = self.app.post(path, data=json.dumps(data), content_type='application/json')
        else:
            resp = self.app.post(path, data=data)
        if is_json_response:
            try:
                o = json.loads(resp.data)
            except JSONDecodeError as e:
                print(resp.data)
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
            print(resp.data)
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

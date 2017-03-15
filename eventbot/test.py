# coding=utf-8
import bot
import simplejson
import unittest


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = bot.app.test_client()

    def tearDown(self):
        pass

    def test_webhook_application_form(self):
        rv = self.app.post('/webhook/application_form', data=build_form_payload())
        # print 'rv.data', rv.data
        o = simplejson.loads(rv.data)
        assert o['status'] == 'ok', o['status']

    # @unittest.skip("testing skipping")
    def test_webhook_eventbrite(self):
        data = {
            'test': True
        }
        rv = self.app.post('/webhook/eventbrite', data=simplejson.dumps(data), content_type='application/json')
        o = simplejson.loads(rv.data)
        assert o['status'] == 'ok', o['status']
        assert o['data']['test'] is True, o

    # @unittest.skip("testing skipping")
    def test_webhook_mailchimp(self):
        data = {
            'test': True
        }
        resp = self.app.post('/webhook/mailchimp', data=simplejson.dumps(data), content_type='application/json')
        resp_data = resp.data
        o = simplejson.loads(resp_data)
        assert o['status'] == 'ok', o['status']
        assert o['data']['test'] is True, o


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

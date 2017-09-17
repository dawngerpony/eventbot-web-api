import requests
import requests_mock
import unittest

# with requests_mock.Mocker() as m:
    # m.get('https://us2.api.mailchimp.com/3.0/lists', text='resp')
    # m.get('https://www.eventbriteapi.com/v3/users/me/owned_events/?expand=none', text='resp')
    # print(requests.get('https://us2.api.mailchimp.com/3.0/lists?foo=bar').text)

# print(requests.get('https://us2.api.mailchimp.com/3.0/lists?foo=bar').text)


@requests_mock.Mocker()
class ApiTestCase(unittest.TestCase):

    # def test_example(self, m):
    #     assert True is False

    def test_example(self, m):
        url = 'http://www.test.com'
        expected_text = 'resp'
        m.register_uri('GET', url, text=expected_text)
        assert _get(url).text == expected_text


def _get(url):
    return requests.get(url)

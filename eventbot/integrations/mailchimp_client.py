#!/usr/bin/env python
from requests.auth import HTTPBasicAuth
import logging
import requests
import settings

# http://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/
REGION = "us2"
BASE_URL = 'https://{}.api.mailchimp.com/3.0'.format(REGION)

log = logging.getLogger(__name__)


def check_interest(email, list_name, interest_category_name, interest_name):
    """ Check whether the specified email address is in the list and has the interest.
    """
    search_result = mc.search(email)
    members = search_result['exact_matches']['members']
    if len(members) > 1:
        raise TooManyFoundException("Number of exact matches should never be greater than 1!")
    if len(members) < 1:
        raise NotFoundException("email {} not found in the database".format(email))
    interest_id = mc.lookup_interest_id(list_name, interest_category_name, interest_name)
    return members[0]['interests'].get(interest_id, False)

    # return search_result['exact_matches']['members']


class TooManyFoundException(Exception):
    pass


class NotFoundException(Exception):
    pass


class MailChimpClient:

    apikey = ''

    reference_data = {
        'lists': {

        }
    }

    def __init__(self, apikey):
        self.apikey = apikey

    def search(self, email):
        """ Search for a member by email.
        """
        path = '/search-members?query={}'.format(email)
        o = self._get(path=path)
        return o

    def lookup_interest_id(self, list_name, interest_category_name, interest_name):
        list_id = self.lookup_list_id(list_name)
        interest_category_id = self.lookup_interest_category_id(list_name, interest_category_name)
        o = self.get_interests(list_id, interest_category_id)
        name_id_map = {l['name']: l['id'] for l in o['interests']}
        return name_id_map.get(interest_name, False)

    def lookup_interest_category_id(self, list_name, interest_category_name):
        list_id = self.lookup_list_id(list_name)
        o = self.get_interest_categories(list_id)
        name_id_map = {l['title']: l['id'] for l in o['categories']}
        return name_id_map.get(interest_category_name, False)

    def lookup_list_id(self, name):
        lists = self.get_lists()
        name_id_map = {l['name']: l['id'] for l in lists['lists']}
        return name_id_map.get(name, False)

    def get_interests(self, list_id, interest_category_id):
        path = '/lists/{}/interest-categories/{}/interests'.format(list_id, interest_category_id)
        interests = self._get(path)
        log.debug('{} interest/s returned for list_id={} interest_category_id={}'.format(
            len(interests['interests']),
            list_id,
            interest_category_id)
        )
        return interests

    def get_interest_categories(self, list_id):
        path = '/lists/{}/interest-categories'.format(list_id)
        interest_categories = self._get(path)
        log.debug('{} interest category/ies returned'.format(len(interest_categories['categories'])))
        return interest_categories

    def get_lists(self):
        path = '/lists'
        lists = self._get(path)
        log.debug('{} list/s returned'.format(len(lists['lists'])))
        return lists

    def _get(self, path):
        url = '{}{}'.format(BASE_URL, path)
        log.debug(url)
        resp = requests.get(url, headers={'Authorization': 'Basic {}'.format(self.apikey)})
        return resp.json()


mc = MailChimpClient(settings.MAILCHIMP_APIKEY)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import pprint
    import sys
    test_apikey = sys.argv[1]
    argv = sys.argv
    mc = MailChimpClient(apikey=test_apikey)
    pp = pprint.PrettyPrinter(indent=4)
    result = mc.check_interest(email=argv[2], list_name=argv[3], interest_category_name=argv[4], interest_name=argv[5])
    pp.pprint(result)

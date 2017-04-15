#!/usr/bin/env python
import logging

import requests
import requests_cache

import eventbot.integrations.defaults

# http://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/
REGION = "us2"
BASE_URL = 'https://{}.api.mailchimp.com/3.0'.format(REGION)

log = logging.getLogger(__name__)


class TooManyFoundException(Exception):
    pass


class NotFoundException(Exception):
    pass


class MailChimpClient:

    api_key = ''

    def __init__(self, api_key, cache_timeout=eventbot.integrations.defaults.REQUESTS_CACHE_TIMEOUT):
        self.api_key = api_key
        requests_cache.install_cache('mailchimp', expire_after=cache_timeout)

    def check_interest(self, email, list_name, interest_category_name, interest_name):
        """ Check whether the specified email address is in the list and has the interest.
        """
        search_result = self.search(email)
        members = search_result['exact_matches']['members']
        if len(members) > 1:
            raise TooManyFoundException("Number of exact matches should never be greater than 1!")
        if len(members) < 1:
            # alt_search_result = self.search(email, alldata=True)
            raise NotFoundException("email {} not found in the database".format(email))
        interest_id = self.lookup_interest_id(list_name, interest_category_name, interest_name)
        return members[0]['interests'].get(interest_id, False)

    def search(self, email, alldata=False):
        """ Search for a member by email.
        """
        if alldata:
            path = '/search-members?query=alldata:{}'.format(email)
        else:
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
        resp = requests.get(url, headers={'Authorization': 'Basic {}'.format(self.api_key)})
        return resp.json()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import pprint
    import sys
    test_apikey = sys.argv[1]
    arg = sys.argv
    pp = pprint.PrettyPrinter(indent=4)
    # result = mc.check_interest(**sys.argv[2])
    # pp.pprint(result)

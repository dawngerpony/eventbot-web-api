import logging

import eventbrite
import requests
import requests_cache
import simplejson

import eventbot.integrations.defaults

log = logging.getLogger(__name__)


class EventbriteClient:

    eventbrite_sdk_client = None

    def __init__(self, eventbrite_oauth_token, cache_timeout=eventbot.integrations.defaults.REQUESTS_CACHE_TIMEOUT):
        self.eventbrite_sdk_client = eventbrite.Eventbrite(eventbrite_oauth_token)
        requests_cache.install_cache('eventbot', expire_after=cache_timeout)

    def get_event_attendees(self, event_id):
        first_page_data = self.eventbrite_sdk_client.get_event_attendees(event_id=event_id)
        if 'error' in first_page_data:
            raise Exception(simplejson.dumps(first_page_data))
        assert 'page_count' in first_page_data.get('pagination', {}), simplejson.dumps(first_page_data)
        page_count = first_page_data['pagination']['page_count']
        object_count = first_page_data['pagination']['object_count']
        log.debug(first_page_data['pagination'])
        if page_count > 1:
            batch_urls = []
            for i in range(page_count):
                batch_urls.append({
                    "method": "GET",
                    "relative_url": "/events/{0}/attendees/?page={1}".format(event_id, i+1)
                })
            data = self.get_batch(batch_urls)
            attendees = []
            i = 1
            for page in data:
                log.debug("Processing page {0}".format(i))
                attendees += page['attendees']
                i += 1
        else:
            attendees = first_page_data['attendees']
        log.debug("first_page_data['pagination']: {}".format(simplejson.dumps(first_page_data['pagination'])))
        assert len(attendees) == object_count,\
            "len(attendees)={0}, object_count={1}".format(len(attendees), object_count)
        debug("Number of attendees", len(attendees))
        return attendees

    def get_url(self, url):
        resp = requests.get(url, headers=self.eventbrite_sdk_client.headers)
        data = resp.json()
        log.debug("data: {}".format(data))
        return data

    def get_batch(self, batch_urls):
        endpoint_url = "{0}batch/".format(eventbrite.utils.EVENTBRITE_API_URL)
        log.debug("Batch URLs: {0}".format(simplejson.dumps(batch_urls)))
        post_data = {"batch": simplejson.dumps(batch_urls)}
        response = requests.post(
            endpoint_url,
            data=simplejson.dumps(post_data),
            headers=self.eventbrite_sdk_client.headers
        )
        if response.status_code != 200:
            raise Exception(response.content)
        if 'error' in response:
            raise Exception(simplejson.dumps(response.content))
        response_data = response.json()
        debug("Number of responses received", len(response_data))
        # debug("response_data", response_data)
        assert_len(response_data, batch_urls, "response_data/batch_urls")
        # responses = [simplejson.loads(item['body']) for item in response_data]
        responses = []
        for item in response_data:
            responses.append(simplejson.loads(item['body']))
        debug("Number of responses processed", len(responses))
        assert_len(responses, response_data, "responses/response_data")
        return responses


def debug(text, data):
    log.debug("{0}: {1}".format(text, simplejson.dumps(data)))


def assert_len(x, y, text):
    assert len(x) == len(y), "{0}: len(x)={1}, len(y)={2}".format(text, len(x), len(y))

from datetime import datetime
import dateutil.parser
import eventbrite
import logging
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

    def get_event_snippets(self, statuses=['live']):
        """ Generate a set of 'snippets' for all the user's events for a
            set of status values (defaults to 'live' events).
        """
        snippets = []
        user_events = self.get_user_owned_events()
        for e in [e for e in user_events['events'] if e['status'] in statuses]:
            ticket_classes = self.eventbrite_sdk_client.get_event_ticket_classes(event_id=e['id'])
            snippets.append(
                {
                    'name': e['name']['text'],
                    'id': e['id'],
                    'status': e['status'],
                    'start': e['start'],
                    'days_remaining': calculate_days_remaining(e),
                    'quantity_sold': calculate_quantity_sold(ticket_classes['ticket_classes']),
                    'capacity': e['capacity']
                }
            )
        return snippets

    def get_user_owned_events(self):
        """
        Get events owned by current user.
        :return:
        """
        data = self.eventbrite_sdk_client.get_user_owned_events(id='me')
        if 'error' in data:
            raise Exception(simplejson.dumps(data))
        assert 'page_count' in data.get('pagination', {}), simplejson.dumps(data)
        if data['pagination']['page_count'] > 1:
            raise Exception("There are {0} pages of data".format(data['page_count']))
        return data

    def get_event_attendees(self, event_id):
        """
        Returns a list of event attendees.
        :param event_id: the ID of the event
        :return:
        """
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


def calculate_days_remaining(event, current_datetime=None):
    start_date = event['start']['utc']
    d0 = dateutil.parser.parse(start_date, ignoretz=True)
    if current_datetime is not None:
        d1 = dateutil.parser.parse(current_datetime, ignoretz=True)
    else:
        d1 = datetime.now()
    return (d0 - d1).days


def calculate_quantity_sold(ticket_classes):
    return sum([int(tc['quantity_sold']) for tc in ticket_classes])

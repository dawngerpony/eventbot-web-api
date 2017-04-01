import eventbrite
from datetime import datetime

import dateutil.parser
import logging
import requests
import settings
import simplejson


eventbrite_sdk_client = eventbrite.Eventbrite(settings.EVENTBRITE_OAUTH_TOKEN)


def get_event_attendees(event_id):
    first_page_data = eventbrite_sdk_client.get_event_attendees(event_id=event_id)
    if 'error' in first_page_data:
        raise Exception(simplejson.dumps(first_page_data))
    assert 'page_count' in first_page_data.get('pagination', {}), simplejson.dumps(first_page_data)
    page_count = first_page_data['pagination']['page_count']
    object_count = first_page_data['pagination']['object_count']
    logging.debug(first_page_data['pagination'])
    if page_count > 1:
        batch_urls = []
        for i in range(page_count):
            batch_urls.append({
                "method": "GET",
                "relative_url": "/events/{0}/attendees/?page={1}".format(event_id, i+1)
            })
        data = get_batch(batch_urls)
        attendees = []
        i = 1
        for page in data:
            logging.debug("Processing page {0}".format(i))
            attendees += page['attendees']
            i += 1
    else:
        attendees = first_page_data['attendees']
    assert len(attendees) == object_count, "len(attendees)={0}, object_count={1}".format(len(attendees), object_count)
    debug("Number of attendees", len(attendees))
    return attendees


def get_batch(batch_urls):
    endpoint_url = "{0}batch/".format(eventbrite.utils.EVENTBRITE_API_URL)
    logging.debug("Batch URLs: {0}".format(simplejson.dumps(batch_urls)))
    post_data = {"batch": simplejson.dumps(batch_urls)}
    response = requests.post(
        endpoint_url,
        data=simplejson.dumps(post_data),
        headers=eventbrite_sdk_client.headers
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
    logging.debug("{0}: {1}".format(text, simplejson.dumps(data)))


def assert_len(x, y, text):
    assert len(x) == len(y), "{0}: len(x)={1}, len(y)={2}".format(text, len(x), len(y))

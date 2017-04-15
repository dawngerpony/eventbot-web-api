#!/usr/bin/env python
import logging
import pprint

import click
import requests
import simplejson as json

from eventbot import settings, fixtures

log = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


@click.command()
@click.option('--base_url', default='http://localhost:5000', help='Base URL for HTTP requests')
@click.option('--event_id', default='123456789', help='Eventbrite event ID')
@click.option('--attendee_id', default='123456789', help='Eventbrite attendee ID')
def run(base_url, event_id, attendee_id):
    data = json.loads(fixtures.EVENTBRITE_ATTENDEE_UPDATED)
    data['api_url'] = 'https://www.eventbriteapi.com/v3/events/{}/attendees/{}/'.format(event_id, attendee_id)
    # pp.pprint(data)
    url = "{}/webhook/eventbrite".format(base_url)
    resp = requests.post(url, json=data)
    log.info(resp.status_code)

if __name__ == '__main__':
    logging.basicConfig(format=settings.CLI_LOG_FORMAT, level=logging.DEBUG)
    run()

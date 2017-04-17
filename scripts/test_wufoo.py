#!/usr/bin/env python
import logging
import pprint

import click
import requests

from eventbot import settings, test

log = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


@click.command()
@click.option('--base_url', default='http://localhost:5000', help='Base URL for HTTP requests')
# @click.option('--event_id', default='123456789', help='Eventbrite event ID')
# @click.option('--attendee_id', default='123456789', help='Eventbrite attendee ID')
def run(base_url):
    data = test.build_form_payload()
    # data['api_url'] = 'https://www.eventbriteapi.com/v3/events/{}/attendees/{}/'.format(event_id, attendee_id)
    # pp.pprint(data)
    url = "{}/webhook/application_form".format(base_url)
    resp = requests.post(url, data=data)
    log.info(resp.status_code)

if __name__ == '__main__':
    logging.basicConfig(format=settings.CLI_LOG_FORMAT, level=logging.DEBUG)
    run()

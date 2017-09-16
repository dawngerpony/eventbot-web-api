#!/usr/bin/env python
from __future__ import print_function
import click
import logging
import pprint
import requests

from eventbot import settings, test, test_fixtures, app

log = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


@click.command()
@click.option('--base_url', default='http://localhost:5000', help='Base URL for HTTP requests')
@click.option('--event_id', default='', help='Eventbrite event ID')
def run(base_url, event_id):
    data = test_fixtures.ROUTES_WEB_HOOK_SLACK_SLASH_COMMAND_ATTENDEES_EXAMPLE_1
    data['text'] = event_id
    url = "{}{}".format(base_url, app.routes.ROUTES_WEB_HOOK_SLACK_SLASH_COMMAND_ATTENDEES)
    resp = requests.post(url, data=data)
    log.info(resp.status_code)
    print(resp.content)


if __name__ == '__main__':
    logging.basicConfig(format=settings.CLI_LOG_FORMAT, level=logging.DEBUG)
    run()

#!/usr/bin/env python
import click
import logging
import pprint
import requests
import urllib

from eventbot import settings, test, test_fixtures

log = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


@click.command()
@click.option('--base_url', default='http://localhost:5000', help='Base URL for HTTP requests')
def run(base_url):
    data = test_fixtures.SLACK_ACTION_ENDPOINT_EXAMPLE_1
    email = urllib.quote(settings.MAILCHIMP_DEFAULT_EMAIL)
    data = data.replace('application_form_action', email)
    url = "{}/slack/action-endpoint".format(base_url)
    resp = requests.post(url, data=data)
    log.info(resp.status_code)
    print resp.content

if __name__ == '__main__':
    logging.basicConfig(format=settings.CLI_LOG_FORMAT, level=logging.DEBUG)
    run()

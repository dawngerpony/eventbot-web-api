#!/usr/bin/env python
from eventbot import fixtures, settings
import click
import logging
import pprint
import requests
import simplejson as json

log = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)


@click.command()
@click.option('--base_url', default='http://localhost:5000', help='Base URL for HTTP requests')
@click.option('--order_id', default='123456789', help='Eventbrite order ID')
def run(base_url, order_id):
    data = json.loads(fixtures.EVENTBRITE_ORDER_PLACED)
    data['api_url'] = 'https://www.eventbriteapi.com/v3/orders/{}'.format(order_id)
    # pp.pprint(data)
    url = "{}/webhook/eventbrite".format(base_url)
    resp = requests.post(url, json=data)
    log.info(resp.status_code)

if __name__ == '__main__':
    logging.basicConfig(format=settings.CLI_LOG_FORMAT, level=logging.DEBUG)
    run()

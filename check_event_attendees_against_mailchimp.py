#!/usr/bin/env python
from collections import Counter
from eventbot.integrations.mailchimp_client import NotFoundException
import click
import eventbot.integrations.eventbrite_client as eb
import eventbot.integrations.mailchimp_client as mc
import logging
import settings
import simplejson as json

log = logging.getLogger(__name__)


def check_attendee(a):
    """ Check one attendee against MailChimp.
    """
    profile = a['profile']
    email = profile['email']
    is_member = False
    is_socialite = False
    try:
        is_member = mc.check_interest(
            email,
            settings.MAILCHIMP_DEFAULT_LIST,
            settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
            'Members'
        )
        is_socialite = mc.check_interest(
            email,
            settings.MAILCHIMP_DEFAULT_LIST,
            settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
            'Socialites'
        )
    except NotFoundException as e:
        log.warn(e.message)
    if is_member and is_socialite:
        log.warn("Attendee {} is marked as a member and a socialite!".format(profile['email']))
    log.info("Checked {} {} (email={}): Member={} Socialite={}".format(
        profile['first_name'],
        profile['last_name'],
        profile['email'],
        is_member,
        is_socialite
    ))


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    pass


@click.command()
@click.option('--input_filename', default='attendees.json', help='filename containing JSON attendee data')
def check(input_filename):
    with open(input_filename, 'r') as f:
        attendees = json.load(f)
    for a in attendees:
        check_attendee(a)
    duplicates = check_duplicates([a['profile']['email'] for a in attendees])
    log.info("duplicates ({}): {}".format(len(duplicates), duplicates))


def check_duplicates(emails):
    return [k for k, v in Counter(emails).items() if v > 1]


@click.command()
@click.option('--output_filename', default='attendees.json', help='output filename to write the JSON attendee data')
@click.argument('eid')
def download(eid, output_filename):
    attendees = eb.get_event_attendees(event_id=eid)
    with open(output_filename, 'w') as f:
        json.dump(attendees, f, indent=2)
    log.info('Attendee data ({} records) written to {}'.format(len(attendees), output_filename))

cli.add_command(download)
cli.add_command(check)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

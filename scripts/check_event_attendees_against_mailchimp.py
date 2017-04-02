#!/usr/bin/env python
from collections import Counter
from eventbot import settings
from eventbot.integrations.mailchimp_client import NotFoundException
from eventbot.integrations import eventbrite_client, mailchimp_client
import click
import logging
import simplejson as json

log = logging.getLogger(__name__)


def check_attendees(attendees):
    results = {
        'attendees': [],
        'totals': {}
    }
    for a in attendees:
        results['attendees'].append(check_attendee(a))
    results['duplicates'] = check_duplicates([a['profile']['email'] for a in attendees])
    log.debug("duplicates ({}): {}".format(len(results['duplicates']), results['duplicates']))
    results['totals'] = {
        'attendees': len(results['attendees']),
        'socialites': len([a for a in results['attendees'] if a['is_socialite'] is True]),
        'members': len([a for a in results['attendees'] if a['is_member'] is True]),
        'duplicates': len(results['duplicates']),
        'not_found': len([a for a in results['attendees'] if a['found'] is False]),
    }
    return results


def check_attendee(a):
    """ Check one Eventbrite attendee against MailChimp.
    """
    o = {
        'email': a['profile']['email'],
        'found': False,
        'is_socialite': False,
        'is_member': False
    }
    mc = mailchimp_client.MailChimpClient(settings.MAILCHIMP_APIKEY)
    try:
        o['is_member'] = mc.check_interest(
            a['profile']['email'],
            settings.MAILCHIMP_DEFAULT_LIST,
            settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
            'Members'
        )
        o['is_socialite'] = mc.check_interest(
            a['profile']['email'],
            settings.MAILCHIMP_DEFAULT_LIST,
            settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
            'Socialites'
        )
        o['found'] = True
    except NotFoundException as e:
        log.debug(e.message)
    if o['found'] is True:
        if o['is_member'] and o['is_socialite']:
            log.warn("Attendee {} is marked as a member and a socialite!".format(a['profile']['email']))
        if o['is_member'] and a['ticket_class_name'].lower() == 'socialite'\
                or o['is_socialite'] and a['ticket_class_name'].lower() == 'member':
            o['has_correct_ticket'] = False
    log.debug("Checked {} {} (email={}): Member={} Socialite={}".format(
        a['profile']['first_name'],
        a['profile']['last_name'],
        a['profile']['email'],
        o['is_member'],
        o['is_socialite']
    ))
    return o


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    pass


@click.command()
@click.option('--eid', default='123', help='Eventbrite event ID')
def check(eid):
    """ Download and check attendee data.
    """
    click.echo("Downloading from Eventbrite...")
    eb = eventbrite_client.EventbriteClient(settings.EVENTBRITE_OAUTH_TOKEN)
    attendees = eb.get_event_attendees(event_id=eid)
    click.echo("Checking attendees against MailChimp...")
    report = check_attendees(attendees)
    click.echo("Report: {} attendees: {} socialites, {} members, {} duplicate(s), {} not found in database".format(
        report['totals']['attendees'],
        report['totals']['socialites'],
        report['totals']['members'],
        report['totals']['duplicates'],
        report['totals']['not_found'],
    ))
    click.echo("Duplicates:\n\t{}".format('\n\t'.join(report['duplicates'])))
    click.echo("Not found:\n\t{}".format('\n\t'.join([a['email'] for a in report['attendees'] if a['found'] is False])))


@click.command()
@click.option('--input_filename', default='attendees.json', help='filename containing JSON attendee data')
@click.option('--download', default=False, help='whether to also download')
def check_file(input_filename):
    """ Check attendee data from a file.
    """
    with open(input_filename, 'r') as f:
        attendees = json.load(f)
    check_attendees(attendees)


def check_duplicates(emails):
    return [k for k, v in Counter(emails).items() if v > 1]


@click.command()
@click.option('--save', default=False, help='save to file')
@click.option('--output_filename', default='attendees.json', help='output filename to write the JSON attendee data')
@click.argument('eid')
def download(eid, output_filename):
    eb = eventbrite_client.EventbriteClient(settings.EVENTBRITE_OAUTH_TOKEN)
    attendees = eb.get_event_attendees(event_id=eid)
    with open(output_filename, 'w') as f:
        json.dump(attendees, f, indent=2)
    log.info('Attendee data ({} records) written to {}'.format(len(attendees), output_filename))
    return attendees


cli.add_command(check)
cli.add_command(download)
cli.add_command(check_file)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

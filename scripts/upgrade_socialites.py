#!/usr/bin/env python
import click
import logging
import pprint
import simplejson as json

from eventbot import settings
from eventbot.app.mailchimp import api_client as mailchimp_client

log = logging.getLogger(__name__)

pp = pprint.PrettyPrinter(indent=4)


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    pass


@click.command()
def clear_upgraded_segment():
    """ Download and check attendee data.
    """
    interest_name = settings.MAILCHIMP_INTEREST_NAME_UPGRADED
    click.echo("Finding members of the '{}' segment...".format(interest_name))
    mc = mailchimp_client.MailChimpInterestManager(
        mailchimp_client.MailChimpClient(settings.MAILCHIMP_APIKEY),
        settings.MAILCHIMP_DEFAULT_LIST,
        settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY
    )
    members = mc.lookup_members_by_interest(interest_name)
    log.info("{} member(s) found in {} segment".format(len(members['members']), interest_name))
    member_email_addresses = [m['email_address'] for m in members['members']]
    pp.pprint(member_email_addresses)
    for m in members['members']:
        mc.remove_interest(m['id'], interest_name)


# @click.command()
def lookup_upgraded_segment():
    """ Download and check attendee data.
    """
    click.echo("Finding segment...")
    mc = mailchimp_client.MailChimpClient(settings.MAILCHIMP_APIKEY)
    interest_id = mc.lookup_interest_id(
        settings.MAILCHIMP_DEFAULT_LIST,
        settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
        settings.MAILCHIMP_INTEREST_NAME_UPGRADED
    )
    return interest_id

# cli.add_command(lookup_upgraded_segment)
cli.add_command(clear_upgraded_segment)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

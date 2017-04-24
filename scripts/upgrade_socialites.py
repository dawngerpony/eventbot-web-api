#!/usr/bin/env python
import click
import logging
import pprint
import requests
import sys

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


@click.command()
@click.argument('email_address')
def upgrade(email_address):
    """ Upgrade a single person from socialite to member.
    """
    click.echo("Upgrading {} from socialite to member...".format(email_address))
    mc = mailchimp_client.MailChimpInterestManager(
        mailchimp_client.MailChimpClient(settings.MAILCHIMP_APIKEY),
        settings.MAILCHIMP_DEFAULT_LIST,
        settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY
    )
    try:
        member = mc.get_member(email_address)
    except requests.exceptions.HTTPError as e:
        click.echo("Error: could not find {} in database (message='{}')".format(email_address, e.message))
        sys.exit(1)
    mc.remove_interest(member['id'], settings.MAILCHIMP_INTEREST_NAME_SOCIALITE)
    mc.add_interest(member['id'], settings.MAILCHIMP_INTEREST_NAME_MEMBER)
    mc.add_interest(member['id'], settings.MAILCHIMP_INTEREST_NAME_UPGRADED)


@click.command()
@click.argument('filename')
def upgrade_file(filename):
    """ Upgrade a list of users from a file from socialite to member.
    """
    mc = mailchimp_client.MailChimpInterestManager(
        mailchimp_client.MailChimpClient(settings.MAILCHIMP_APIKEY),
        settings.MAILCHIMP_DEFAULT_LIST,
        settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY
    )
    with open(filename) as f:
        email_address_list = f.readlines()
    email_address_list = map(str.strip, email_address_list)
    for email_address in email_address_list:
        try:
            member = mc.get_member(email_address)
        except requests.exceptions.HTTPError as e:
            click.echo("Error: could not find {} in database (message='{}')".format(email_address, e.message))
            sys.exit(1)
        mc.remove_interest(member['id'], settings.MAILCHIMP_INTEREST_NAME_SOCIALITE)
        mc.add_interest(member['id'], settings.MAILCHIMP_INTEREST_NAME_MEMBER)
        mc.add_interest(member['id'], settings.MAILCHIMP_INTEREST_NAME_UPGRADED)
        click.echo('Upgraded {}'.format(email_address))


@click.command()
@click.argument('filename')
def find_list_members(filename):
    """ Upgrade a list of users from a file from socialite to member.
    """
    mc = mailchimp_client.MailChimpInterestManager(
        mailchimp_client.MailChimpClient(settings.MAILCHIMP_APIKEY),
        settings.MAILCHIMP_DEFAULT_LIST,
        settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY
    )
    with open(filename) as f:
        email_address_list = f.readlines()
    email_address_list = map(str.strip, email_address_list)
    for email_address in email_address_list:
        try:
            mc.get_member(email_address.strip())
            click.echo("Found {} in database (message='{}')".format(email_address, e.message))
        except requests.exceptions.HTTPError as e:
            click.echo("Error: could not find {} in database (message='{}')".format(email_address, e.message))

cli.add_command(clear_upgraded_segment)
cli.add_command(find_list_members)
cli.add_command(upgrade)
cli.add_command(upgrade_file)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

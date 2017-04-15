#####################
# Attendee reporter #
#####################

import eventbot.settings
import mailchimp.api_client as mailchimp_client


def check_interests(email, interests):
    """ Check an Eventbrite attendee against a set of interests (groups) in MailChimp.
    """
    mc = mailchimp_client.MailChimpClient(api_key=eventbot.settings.MAILCHIMP_APIKEY)
    o = {}
    for interest in interests:
        has_interest = mc.check_interest(
            email,
            eventbot.settings.MAILCHIMP_DEFAULT_LIST,
            eventbot.settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
            interest
        )
        o[interest] = has_interest
    return o


def check_membership(eb_attendee_url):
    """ Check membership status of an event attendee.
    """
    log.info("Checking membership for url={}".format(eb_attendee_url))
    eb = eventbrite_client.EventbriteClient(eventbot.settings.EVENTBRITE_OAUTH_TOKEN)
    attendee = eb.get_url(eb_attendee_url)
    log.info('attendee: {}'.format(json.dumps(attendee)))
    email = attendee['profile']['email']
    try:
        check_interests(email, ["Socialites", "Members"])
    except NotFoundException as e:
        log.warn(e.message)
        slack.post_warning_to_webhook("{} just bought a ticket for an event but is not in our database!".format(email))
    event_id = attendee['event_id']

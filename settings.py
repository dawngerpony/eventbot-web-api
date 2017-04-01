# settings.py
from os.path import join, dirname
from dotenv import load_dotenv

import logging
import os

log = logging.getLogger(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

EVENTBRITE_OAUTH_TOKEN = os.environ.get('EVENTBRITE_OAUTH_TOKEN')
EVENTBRITE_TEST_EVENT_ID = os.environ.get('EVENTBRITE_TEST_EVENT_ID')
EVENTBRITE_EVENT_STATS_CHANNELS = os.environ.get('EVENTBRITE_EVENT_STATS_CHANNELS')

MAILCHIMP_APIKEY = os.environ.get('MAILCHIMP_APIKEY')
MAILCHIMP_DEFAULT_LIST = os.environ.get('MAILCHIMP_DEFAULT_LIST')
MAILCHIMP_DEFAULT_INTEREST_CATEGORY = os.environ.get('MAILCHIMP_DEFAULT_INTEREST_CATEGORY')

SLACK_CHANNELS = os.environ.get('SLACK_CHANNELS', 'general,eventbot-test').split(',')
SLACK_BOT_NAME = os.environ.get('SLACK_BOT_NAME')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = os.environ.get('BOT_ID')

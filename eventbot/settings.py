# settings.py
from os.path import join, dirname
from dotenv import load_dotenv

import logging
import os

log = logging.getLogger(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CLI_LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_FORMAT = '%(filename)s:%(lineno)s - %(funcName)20s() [%(levelname)s] %(message)s'

EVENTBRITE_EVENT_STATS_CHANNELS = os.environ.get('EVENTBRITE_EVENT_STATS_CHANNELS')
EVENTBRITE_OAUTH_TOKEN = os.environ.get('EVENTBRITE_OAUTH_TOKEN')
EVENTBRITE_TEST_EVENT_ID = os.environ.get('EVENTBRITE_TEST_EVENT_ID')

MAILCHIMP_APIKEY = os.environ.get('MAILCHIMP_APIKEY')
MAILCHIMP_DEFAULT_INTEREST_CATEGORY = os.environ.get('MAILCHIMP_DEFAULT_INTEREST_CATEGORY')
MAILCHIMP_DEFAULT_LIST = os.environ.get('MAILCHIMP_DEFAULT_LIST')

REQUESTS_CACHE_TIMEOUT = os.environ.get('REQUESTS_CACHE_TIMEOUT', 300)

SLACK_BOT_ID = os.environ.get('BOT_ID')
SLACK_BOT_NAME = os.environ.get('SLACK_BOT_NAME')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_CHANNELS = os.environ.get('SLACK_CHANNELS', 'general,eventbot-test').split(',')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')

# coding=utf-8
import urllib
import simplejson as json

EVENTBRITE_ORDER_PLACED = '''
{
    "config": {
        "action": "order.placed",
        "webhook_id": "123456",
        "user_id": "123456789012",
        "endpoint_url": "https://test-app-12345.herokuapp.com/webhook/eventbrite"
    },
    "api_url": "https://www.eventbriteapi.com/v3/orders/123456789/"
}
'''

EVENTBRITE_ATTENDEE_UPDATED = '''
{
    "config": {
        "action": "attendee.updated",
        "webhook_id": "123456",
        "user_id": "123456789012",
        "endpoint_url": "https://test-app-12345.herokuapp.com/webhook/eventbrite"
    }, "api_url": "https://www.eventbriteapi.com/v3/events/12345678901/attendees/762511533/"
}
'''

EVENTBRITE_ORDER_UPDATED = '''
{
    "config": {
        "action": "order.updated",
        "webhook_id": "123456",
        "user_id": "123456789012",
        "endpoint_url": "https://test-app-12345.herokuapp.com/webhook/eventbrite"
    }, "api_url": "https://www.eventbriteapi.com/v3/orders/123456789/"
}
'''

EVENTBRITE_TICKET_CLASS_UPDATED = '''
{
    "config": {
        "action": "ticket_class.updated",
        "webhook_id": "346362",
        "user_id": "163230244025",
        "endpoint_url": "https://test-app-12345.herokuapp.com/webhook/eventbrite"
    }, "api_url": "https://www.eventbriteapi.com/v3/events/12345678901/ticket_classes/61579852/"
}
'''

# SLACK_ACTION_ENDPOINT_EXAMPLE_1 = u'payload=%7B%22' \
#                                   u'actions%22%3A%5B%7B%22name%22%3A%22' \
#                                   u'application_form%22%2C%22type%22%3A%22' \
#                                   u'button%22%2C%22' \
#                                   u'value%22%3A%22' \
#                                   u'approve%22%7D%5D%2C%22' \
#                                   u'callback_id%22%3A%22application_form_action%22%2C%22' \
#                                   u'team%22%3A%7B%22' \
#                                   u'id%22%3A%22T2A1BQ1RU%22%2C%22' \
#                                   u'domain%22%3A%22' \
#                                   u'impudicitia%22%7D%2C%22' \
#                                   u'channel%22%3A%7B%22' \
#                                   u'id%22%3A%22G2YSCQX46%22%2C%22' \
#                                   u'name%22%3A%22' \
#                                   u'privategroup%22%7D%2C%22' \
#                                   u'user%22%3A%7B%22' \
#                                   u'id%22%3A%22U2A1JJH8D%22%2C%22' \
#                                   u'name%22%3A%22dj%22%7D%2C%22' \
#                                   u'action_ts%22%3A%221492430795.492670%22%2C%22' \
#                                   u'message_ts%22%3A%221492430564.758743%22%2C%22' \
#                                   u'attachment_id%22%3A%222%22%2C%22' \
#                                   u'token%22%3A%22PbjaJmgvLt3BYorXkBJKfOCp%22%2C%22' \
#                                   u'is_app_unfurl%22%3Afalse%2C%22' \
#                                   u'original_message%22%3A%7B%22' \
#                                   u'text%22%3A%22%5Cn++++%27téxt%5Cn++++%22%2C%22' \
#                                   u'bot_id%22%3A%22B4ZV9RKDG%22%2C%22' \
#                                   u'attachments%22%3A%5B%7B%22fallback%22%3A%22Required+plain-text+summary+of+the+attachment.%22%2C%22' \
#                                   u'image_url%22%3A%22https%3A%5C%2F%5C%2Fafterpandora.wufoo.com%5C%2Fcabinet%5C%2FbTdjemY5dzFxaGtkczc%3D%5C%2Fqwuslash9hDvwuBennag%253D%5C%2Fsupermariobros.jpg%22%2C%22' \
#                                   u'image_width%22%3A959%2C%22image_height%22%3A467%2C%22image_bytes%22%3A53876%2C%22title%22%3A%22Image+1%22%2C%22' \
#                                   u'id%22%3A1%2C%22color%22%3A%2236a64f%22%7D%2C%7B%22' \
#                                   u'callback_id%22%3A%22application_form_action%22%2C%22' \
#                                   u'fallback%22%3A%22No+action+chosen%22%2C%22' \
#                                   u'text%22%3A%22What+action+should+I+take%3F%22%2C%22' \
#                                   u'id%22%3A2%2C%22color%22%3A%223AA3E3%22%2C%22' \
#                                   u'actions%22%3A%5B%7B%22id%22%3A%221%22%2C%22' \
#                                   u'name%22%3A%22application_form%22%2C%22' \
#                                   u'text%22%3A%22Approve%22%2C%22' \
#                                   u'type%22%3A%22button%22%2C%22' \
#                                   u'value%22%3A%22approve%22%2C%22' \
#                                   u'style%22%3A%22%22%7D%5D%7D%5D%2C%22type%22%3A%22message%22%2C%22' \
#                                   u'subtype%22%3A%22bot_message%22%2C%22' \
#                                   u'ts%22%3A%221492430564.758743%22%7D%2C%22' \
#                                   u'response_url%22%3A%22https%3A%5C%2F%5C%2Fhooks.slack.com%5C%2Factions%5C%2FT2A1BQ1RU%5C%2F170072243252%5C%2Fw5B4dWoLzIaAEjeCMoWDUKUL%22%7D'

SLACK_ACTION_ENDPOINT_EXAMPLE_1_DECODED = """{
    "action_ts": "1492430795.492670",
    "actions": [
        {
            "name": "application_form",
            "type": "button",
            "value": "approve"
        }
    ],
    "attachment_id": "2",
    "callback_id": "application_form_action",
    "channel": {
        "id": "G2YSCQX46",
        "name": "privategroup"
    },
    "is_app_unfurl": false,
    "message_ts": "1492430564.758743",
    "original_message": {
        "attachments": [
            {
                "color": "36a64f",
                "fallback": "Required+plain-text+summary+of+the+attachment.",
                "id": 1,
                "image_bytes": 53876,
                "image_height": 467,
                "image_url": "https://afterpandora.wufoo.com/cabinet/bTdjemY5dzFxaGtkczc=/qwuslash9hDvwuBennag%3D/supermariobros.jpg",
                "image_width": 959,
                "title": "Image+1"
            },
            {
                "actions": [
                    {
                        "id": "1",
                        "name": "application_form",
                        "style": "",
                        "text": "Approve",
                        "type": "button",
                        "value": "approve"
                    }
                ],
                "callback_id": "application_form_action",
                "color": "3AA3E3",
                "fallback": "No+action+chosen",
                "id": 2,
                "text": "What+action+should+I+take?"
            }
        ],
        "bot_id": "B4ZV9RKDG",
        "subtype": "bot_message",
        "text": "\\n++++'téxt\\n++++",
        "ts": "1492430564.758743",
        "type": "message"
    },
    "response_url": "https://hooks.slack.com/actions/T2A1BQ1RU/170072243252/w5B4dWoLzIaAEjeCMoWDUKUL",
    "team": {
        "domain": "impudicitia",
        "id": "T2A1BQ1RU"
    },
    "token": "PbjaJmgvLt3BYorXkBJKfOCp",
    "user": {
        "id": "U2A1JJH8D",
        "name": "dj"
    }
}
"""

j = json.loads(SLACK_ACTION_ENDPOINT_EXAMPLE_1_DECODED)
s = json.dumps(j)
SLACK_ACTION_ENDPOINT_EXAMPLE_1 = "payload={}".format(urllib.quote(s))

ROUTES_WEB_HOOK_SLACK_SLASH_COMMAND_ATTENDEES_EXAMPLE_1 = """
{
}
"""

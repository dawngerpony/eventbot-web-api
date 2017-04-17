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

SLACK_ACTION_ENDPOINT_EXAMPLE_1 = 'payload=%7B%22' \
                                  'actions%22%3A%5B%7B%22name%22%3A%22' \
                                  'application_form%22%2C%22type%22%3A%22' \
                                  'button%22%2C%22' \
                                  'value%22%3A%22' \
                                  'approve%22%7D%5D%2C%22' \
                                  'callback_id%22%3A%22application_form_action%22%2C%22' \
                                  'team%22%3A%7B%22' \
                                  'id%22%3A%22T2A1BQ1RU%22%2C%22' \
                                  'domain%22%3A%22' \
                                  'impudicitia%22%7D%2C%22' \
                                  'channel%22%3A%7B%22' \
                                  'id%22%3A%22G2YSCQX46%22%2C%22' \
                                  'name%22%3A%22' \
                                  'privategroup%22%7D%2C%22' \
                                  'user%22%3A%7B%22' \
                                  'id%22%3A%22U2A1JJH8D%22%2C%22' \
                                  'name%22%3A%22dj%22%7D%2C%22' \
                                  'action_ts%22%3A%221492430795.492670%22%2C%22' \
                                  'message_ts%22%3A%221492430564.758743%22%2C%22' \
                                  'attachment_id%22%3A%222%22%2C%22' \
                                  'token%22%3A%22PbjaJmgvLt3BYorXkBJKfOCp%22%2C%22' \
                                  'is_app_unfurl%22%3Afalse%2C%22' \
                                  'original_message%22%3A%7B%22' \
                                  'text%22%3A%22%5Cn++++%27text%5Cn++++%22%2C%22' \
                                  'bot_id%22%3A%22B4ZV9RKDG%22%2C%22' \
                                  'attachments%22%3A%5B%7B%22fallback%22%3A%22Required+plain-text+summary+of+the+attachment.%22%2C%22' \
                                  'image_url%22%3A%22https%3A%5C%2F%5C%2Fafterpandora.wufoo.com%5C%2Fcabinet%5C%2FbTdjemY5dzFxaGtkczc%3D%5C%2Fqwuslash9hDvwuBennag%253D%5C%2Fsupermariobros.jpg%22%2C%22' \
                                  'image_width%22%3A959%2C%22image_height%22%3A467%2C%22image_bytes%22%3A53876%2C%22title%22%3A%22Image+1%22%2C%22' \
                                  'id%22%3A1%2C%22color%22%3A%2236a64f%22%7D%2C%7B%22' \
                                  'callback_id%22%3A%22application_form_action%22%2C%22' \
                                  'fallback%22%3A%22No+action+chosen%22%2C%22' \
                                  'text%22%3A%22What+action+should+I+take%3F%22%2C%22' \
                                  'id%22%3A2%2C%22color%22%3A%223AA3E3%22%2C%22' \
                                  'actions%22%3A%5B%7B%22id%22%3A%221%22%2C%22' \
                                  'name%22%3A%22application_form%22%2C%22' \
                                  'text%22%3A%22Approve%22%2C%22' \
                                  'type%22%3A%22button%22%2C%22' \
                                  'value%22%3A%22approve%22%2C%22' \
                                  'style%22%3A%22%22%7D%5D%7D%5D%2C%22type%22%3A%22message%22%2C%22' \
                                  'subtype%22%3A%22bot_message%22%2C%22' \
                                  'ts%22%3A%221492430564.758743%22%7D%2C%22' \
                                  'response_url%22%3A%22https%3A%5C%2F%5C%2Fhooks.slack.com%5C%2Factions%5C%2FT2A1BQ1RU%5C%2F170072243252%5C%2Fw5B4dWoLzIaAEjeCMoWDUKUL%22%7D'

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
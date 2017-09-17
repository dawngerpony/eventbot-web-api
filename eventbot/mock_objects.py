import settings

MAILCHIMP_MOCK_RESPONSE_LISTS = {
    "lists": [
        {
            "name": "foo",
            "id": "bar"
        }
    ]
}

MAILCHIMP_MOCK_RESPONSE_INTEREST_CATEGORIES = {
    "categories": [
        {
            "title": settings.MAILCHIMP_DEFAULT_INTEREST_CATEGORY,
            "id": "foo"
        }
    ]
}


MAILCHIMP_MOCK_RESPONSE_MEMBER = {
    "id": "foo",
    "interests": {
        "foo": True
    }
}

MAILCHIMP_MOCK_RESPONSE_INTERESTS = {
    "interests": [
        {
            "name": "Socialites",
            "id": "foo"
        }
    ]
}

EVENTBRITE_MOCK_RESPONSE_ATTENDEES = {
    "pagination": {
        "page_count": 1,
        "object_count": 1
    },
    "attendees": [
        {
            "profile": {
                "name": "Foo Bar",
                "email": "foo@bar.com"
            },
            "refunded": False,
            "ticket_class_name": "foo"
        }
    ]
}

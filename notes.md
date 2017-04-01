Links
-----

* http://www.wufoo.com/guides/setup-webhooks-in-wufoo-to-get-push-notifications-to-your-apps/

Searching for members in MailChimp
----------------------------------

From http://developer.mailchimp.com/documentation/mailchimp/reference/search-members/:

    curl --request GET \
        --url 'https://usX.api.mailchimp.com/3.0/search-members?query=freddie@' \
        --user 'anystring:apikey' \
        --include

Posting to Slack webhook
------------------------

    curl -X POST $SLACK_WEBHOOK_URL -H 'Content-Type: application/json' -d '{"text": "foo" }'


Sample request from Wufoo
-------------------------

    2017-01-14T13:04:03.567506+00:00 app[web.1]: INFO:app:request data: 
    2017-01-14T13:04:03.567664+00:00 app[web.1]: INFO:app:request form: ImmutableMultiDict([('Field17', u''), ('Field14', u'Other site'), ('Field12', u'My interests'), ('HandshakeKey', u''), ('Field11', u'Myself'), ('Field27', u'Dafydd referral'), ('Field17-url', u''), ('Field3', u'Dafydd name'), ('DateCreated', u'2017-01-14 05:04:00'), ('Field5', u'dafydd@afterpandora.com'), ('Field6', u'DuffX'), ('EntryId', u'924'), ('IP', u'86.155.134.187'), ('CreatedBy', u'public'), ('Field8', u'Fetlife')])
    2017-01-14T13:04:03.567883+00:00 app[web.1]: INFO:app:request headers: Connect-Time: 0
    2017-01-14T13:04:03.567885+00:00 app[web.1]: X-Request-Start: 1484399043565
    2017-01-14T13:04:03.567887+00:00 app[web.1]: X-Request-Id: ac3fb64a-f4b2-411f-a818-08aa37ff8cda
    2017-01-14T13:04:03.567885+00:00 app[web.1]: Content-Length: 277
    2017-01-14T13:04:03.567887+00:00 app[web.1]: Content-Type: application/x-www-form-urlencoded
    2017-01-14T13:04:03.567888+00:00 app[web.1]: Via: 1.1 vegur
    2017-01-14T13:04:03.567901+00:00 app[web.1]: X-Newrelic-Id: VQIHUVRTABADUFlXAAYHVg==
    2017-01-14T13:04:03.567902+00:00 app[web.1]: User-Agent: Wufoo.com
    2017-01-14T13:04:03.567904+00:00 app[web.1]: X-Newrelic-Transaction: PxQCA1RUCVEDB1lbBVNUVFRSFB8EBw8RVU4aV1oKAwNRVlpZCFNRAVYGVENKQV0CUlZXW1NQFTs=
    2017-01-14T13:04:03.567905+00:00 app[web.1]: Accept: */*
    2017-01-14T13:04:03.567905+00:00 app[web.1]: Connection: close
    2017-01-14T13:04:03.567906+00:00 app[web.1]: Host: floating-refuge-91822.herokuapp.com
    2017-01-14T13:04:03.567907+00:00 app[web.1]: X-Forwarded-For: 75.98.93.198
    2017-01-14T13:04:03.567910+00:00 app[web.1]: X-Forwarded-Proto: https
    2017-01-14T13:04:03.567911+00:00 app[web.1]: Total-Route-Time: 0
    2017-01-14T13:04:03.567912+00:00 app[web.1]: 
    2017-01-14T13:04:03.567907+00:00 app[web.1]: X-Forwarded-Port: 443
    2017-01-14T13:04:03.567912+00:00 app[web.1]: 
    2017-01-14T13:04:03.568037+00:00 app[web.1]: INFO:app:d: {"body": "", "status": "ok"}

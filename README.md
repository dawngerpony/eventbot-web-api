eventbot-web-api
================

[![CircleCI](https://circleci.com/gh/duffj/eventbot-web-api.svg?style=svg)](https://circleci.com/gh/duffj/eventbot-web-api)

Eventbot web API.


Pipeline
--------

CircleCI is configured to auto-deploy to Heroku if the build passes.


Local development
-----------------

NB. Tested on a Mac, not on Windows.

### Pre-requisites

* Python 2.7 with virtualenv
* Heroku CLI Toolbelt
* GNU Make

FYI I use [homebrew][1] for most of these things on my Mac. 

### Setup

1. Create a virtualenv: `virtualenv .venv`
1. Enter the env: `. .venv/bin/activate`
1. Install pip requirements: `pip install -r requirements.txt`

### To run locally

    make local

### To run the tests

    make test

### To deploy

The app is deployed automatically to Heroku by CircleCI on
successful build of the `master` branch.


ngrok
-----

To run:

    ngrok http 50000

View the dashboard: [Dashboard](http://localhost:4040/inspect/http)

Technologies
------------

* Python - see [requirements.txt](requirements.txt)
* Heroku
* CircleCI
* ngrok


Tips
----

### Adding a new 'slash command'

1. Go to [https://api.slack.com](https://api.slack.com) / Your Apps / Eventbot / Slash commands.

Links
-----

* https://elements.heroku.com/addons/mongolab
* https://community.nitrous.io/tutorials/deploying-a-flask-application-to-heroku
* [Using ngrok to develop locally for Slack](https://api.slack.com/tutorials/tunneling-with-ngrok)

[1]: https://brew.sh/ "homebrew"

eventbot-web-api
================

[![CircleCI](https://circleci.com/gh/duffj/eventbot-web-api.svg?style=svg)](https://circleci.com/gh/duffj/eventbot-web-api)

Eventbot web API.


Pipeline
--------

CircleCI is configured to auto-deploy to Heroku if the build passes.


To run locally
--------------

    make local


Technologies
------------

* Python
    * Flask web microframework
    * flask-wtf - for forms
    * nosetests2
* Heroku
* CircleCI

Links
-----

* https://elements.heroku.com/addons/mongolab
* https://community.nitrous.io/tutorials/deploying-a-flask-application-to-heroku

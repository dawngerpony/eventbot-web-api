#!/usr/bin/env python

from flask import Flask
from flask_restful import Resource, Api

import settings
from forms import ApplicationForm
from flask_wtf import csrf
from flask_wtf.csrf import CSRFProtect
# from flask_wtf.csrf.CSRFProtect import exempt
import flask
import logging
import requests
import simplejson as json


app = Flask(__name__)
# api = Api(app)
#
#
# class HelloWorld(Resource):
#
#     def get(self):
#         return {'hello': 'world'}
#
#
# api.add_resource(HelloWorld, '/')

app.config.setdefault('WTF_CSRF_CHECK_DEFAULT', False)
app.config.setdefault('WTF_CSRF_ENABLED', False)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# csrf = CSRFProtect(app)
# csrf.exempt('web_hook_application_form')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/webhook/application_form", methods=['POST', 'GET'])
def web_hook_application_form():
    """ Web hook for incoming application forms.
    """
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    logger.info("web_hook_application_form")
    form = ApplicationForm()
    logger.info("request data: {}".format(flask.request.data))
    logger.info("request form: {}".format(flask.request.form))
    logger.info("request headers: {}".format(flask.request.headers))
    d = {
        'status': 'ok',
        'form': flask.request.form
    }
    if form.validate_on_submit():
        d['Field3'] = {
            'data': form.Field3.data,
            'label.field_id': form.Field3.label.field_id,
            'name': form.Field3.name
        }
        text = """
'{}' ({}) submitted an application form.
*Please tell us about yourself:* {}
*What interests you?* {}
""".format(form.Field3.data, form.Field5.data, form.Field11.data, form.Field12.data)

        slack_webhook_obj = {"text": text}
        requests.post(slack_webhook_url, data=json.dumps(slack_webhook_obj))
    logger.info("d: {}".format(json.dumps(d)))
    return flask.jsonify(**d)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

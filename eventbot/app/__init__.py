from errors import InvalidUsage
from flask import Flask, jsonify

app = Flask(__name__)

app.config.setdefault('WTF_CSRF_ENABLED', False)

import routes


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

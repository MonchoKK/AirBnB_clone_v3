#!/usr/bin/python3
""" Instantiates a Flask application & registers BluePrints """
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
import os


# instantiate a Flask application
app = Flask(__name__)
# override strict_slashes behaviour globally
app.url_map.strict_slashes = False
# add CORS to allow cross-origin requests (from 0.0.0.0) ->anywhere
CORS(app, resources={r"/api/v1/*": {"origins": '0.0.0.0'}})
# register app_views Blueprint (include url_prefix
app.register_blueprint(app_views, url_prefix='/api/v1/')


@app.teardown_appcontext
def close_context(self):
    """ tears down current session (done after every request) """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Creates a handler for 404 errors that returns a JSON-formatted
    404 status code response """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000), threaded=True)

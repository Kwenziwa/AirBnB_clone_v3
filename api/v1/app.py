#!/usr/bin/python3
'''
Module that defines the first endpoint.
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    '''
    Method that calls storage.close()
    '''
    storage.close()


cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    '''
    Handler for 404 errors that returns a JSON-formatted 404 response.
    '''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', 5000)),
        threaded=True
    )
#!/usr/bin/python3
'''Contains a Flask web application API.
'''
import os
from api.v1.views import app_views
from flask import jsonify

# Define a route /status on the object app_views that returns a JSON: "status": "OK"
app = Flask(__name__)

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})
    
if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )

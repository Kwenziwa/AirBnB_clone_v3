#!/usr/bin/python3
'''Contains a Flask web application API.
'''
import os
from api.v1.views import app_views
from flask import jsonify

# Define a route /status on the object app_views that returns a JSON: "status": "OK"
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

#!/usr/bin/python3
""" Index module """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a json"""
    return jsonify({"status": "OK"})

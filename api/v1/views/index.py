#!/usr/bin/python3
'''
Module that define the index
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    '''
    Method that return the status of api
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    '''
    Retrieves the number of each object type
    '''
    stats_dict = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats_dict)
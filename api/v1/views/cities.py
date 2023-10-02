#!/usr/bin/python3
'''Contains the cities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_cities(state_id=None, city_id=None):
    '''The method handler for the cities endpoint.
    '''
    handlers = {
        'GET': get_cities,
        'DELETE': remove_city,
        'POST': add_city,
        'PUT': update_city,
    }
    if request.method in handlers:
        return handlers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_cities(state_id=None, city_id=None):
    '''Gets the city with the given id or all cities in
    the state with the given id.
    '''
    if state_id:
        state = storage.get(State, state_id)
        if state:
            mycities = list(map(lambda x: x.to_dict(), state.cities))
            return jsonify(mycities)
    elif city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
    raise NotFound()


def remove_city(state_id=None, city_id=None):
    '''Removes a city with the given id.
    '''
    if city_id:
        mycity = storage.get(City, city_id)
        if mycity:
            storage.delete(mycity)
            if storage_t != "db":
                for place in storage.all(Place).values():
                    if place.city_id == city_id:
                        for review in storage.all(Review).values():
                            if review.place_id == place.id:
                                storage.delete(review)
                        storage.delete(place)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_city(state_id=None, city_id=None):
    '''Adds a new city.
    '''
    mystate = storage.get(State, state_id)
    if not mystate:
        raise NotFound()
    mydata = request.get_json()
    if type(mydata) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in mydata:
        raise BadRequest(description='Missing name')
    mydata['state_id'] = state_id
    mycity = City(**mydata)
    mycity.save()
    return jsonify(mycity.to_dict()), 201


def update_city(state_id=None, city_id=None):
    '''Updates the city with the given id.
    '''
    xkeys = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        mycity = storage.get(City, city_id)
        if mycity:
            mydata = request.get_json()
            if type(mydata) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in mydata.items():
                if key not in xkeys:
                    setattr(mycity, key, value)
            mycity.save()
            return jsonify(mycity.to_dict()), 200
    raise NotFound()

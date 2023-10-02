#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_places(city_id=None, place_id=None):
    '''The method handler for the places endpoint.
    '''
    handlers = {
        'GET': get_places,
        'DELETE': remove_place,
        'POST': add_place,
        'PUT': update_place
    }
    if request.method in handlers:
        return handlers[request.method](city_id, place_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_places(city_id=None, place_id=None):
    '''Gets the place with the given id or all places in
    the city with the given id.
    '''
    if city_id:
        mycity = storage.get(City, city_id)
        if mycity:
            all_my_places = []
            if storage_t == 'db':
                all_my_places = list(mycity.places)
            else:
                all_my_places = list(filter(
                    lambda x: x.city_id == city_id,
                    storage.all(Place).values()
                ))
            places = list(map(lambda x: x.to_dict(), all_my_places))
            return jsonify(places)
    elif place_id:
        myplace = storage.get(Place, place_id)
        if myplace:
            return jsonify(myplace.to_dict())
    raise NotFound()


def remove_place(city_id=None, place_id=None):
    '''Removes a place with the given id.
    '''
    if place_id:
        myplace = storage.get(Place, place_id)
        if myplace:
            storage.delete(myplace)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_place(city_id=None, place_id=None):
    '''Adds a new place.
    '''
    mycity = storage.get(City, city_id)
    if not mycity:
        raise NotFound()
    mydata = request.get_json()
    if type(mydata) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in mydata:
        raise BadRequest(description='Missing user_id')
    auser = storage.get(User, mydata['user_id'])
    if not auser:
        raise NotFound()
    if 'name' not in mydata:
        raise BadRequest(description='Missing name')
    mydata['city_id'] = city_id
    anew_place = Place(**mydata)
    anew_place.save()
    return jsonify(anew_place.to_dict()), 201


def update_place(city_id=None, place_id=None):
    '''Updates the place with the given id.
    '''
    xkeys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    myplace = storage.get(Place, place_id)
    if myplace:
        mydata = request.get_json()
        if type(mydata) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in mydata.items():
            if key not in xkeys:
                setattr(myplace, key, value)
        myplace.save()
        return jsonify(myplace.to_dict()), 200
    raise NotFound()


@app_views.route('/places_search', methods=['POST'])
def find_places():
    '''Finds places based on a list of State, City, or Amenity ids.
    '''
    mydata = request.get_json()
    if type(mydata) is not dict:
        raise BadRequest(description='Not a JSON')
    all_my_places = storage.all(Place).values()
    places = []
    places_id = []
    keys_status = (
        all([
            'states' in mydata and type(mydata['states']) is list,
            'states' in mydata and len(mydata['states'])
        ]),
        all([
            'cities' in mydata and type(mydata['cities']) is list,
            'cities' in mydata and len(mydata['cities'])
        ]),
        all([
            'amenities' in mydata and type(mydata['amenities']) is list,
            'amenities' in mydata and len(mydata['amenities'])
        ])
    )
    if keys_status[0]:
        for state_id in mydata['states']:
            if not state_id:
                continue
            mystate = storage.get(State, state_id)
            if not mystate:
                continue
            for mycity in mystate.cities:
                new_places = []
                if storage_t == 'db':
                    new_places = list(
                        filter(lambda x: x.id not in places_id, mycity.places)
                    )
                else:
                    new_places = []
                    for myplace in all_my_places:
                        if myplace.id in places_id:
                            continue
                        if myplace.city_id == mycity.id:
                            new_places.append(myplace)
                places.extend(new_places)
                places_id.extend(list(map(lambda x: x.id, new_places)))
    if keys_status[1]:
        for city_id in mydata['cities']:
            if not city_id:
                continue
            mycity = storage.get(City, city_id)
            if mycity:
                new_places = []
                if storage_t == 'db':
                    new_places = list(
                        filter(lambda x: x.id not in places_id, mycity.places)
                    )
                else:
                    new_places = []
                    for myplace in all_my_places:
                        if myplace.id in places_id:
                            continue
                        if myplace.city_id == mycity.id:
                            new_places.append(myplace)
                places.extend(new_places)
    del places_id
    if all([not keys_status[0], not keys_status[1]]) or not mydata:
        places = all_my_places
    if keys_status[2]:
        amenity_ids = []
        for amenity_id in mydata['amenities']:
            if not amenity_id:
                continue
            amenity = storage.get(Amenity, amenity_id)
            if amenity and amenity.id not in amenity_ids:
                amenity_ids.append(amenity.id)
        del_indices = []
        for myplace in places:
            place_amenities_ids = list(map(lambda x: x.id, myplace.amenities))
            if not amenity_ids:
                continue
            for amenity_id in amenity_ids:
                if amenity_id not in place_amenities_ids:
                    del_indices.append(myplace.id)
                    break
        places = list(filter(lambda x: x.id not in del_indices, places))
    result = []
    for myplace in places:
        obj = myplace.to_dict()
        if 'amenities' in obj:
            del obj['amenities']
        result.append(obj)
    return jsonify(result)

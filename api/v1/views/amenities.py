#!/usr/bin/python3
'''Contains the amenities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods allowed for the amenities endpoint.'''


@app_views.route('/amenities', methods=ALLOWED_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_amenities(amenity_id=None):
    '''The method handler for the amenities endpoint.
    '''
    handlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenities(amenity_id=None):
    '''Gets the amenity with the given id or all amenities.
    '''
    amenity_list = storage.all(Amenity).values()
    if amenity_id:
        my_res = list(filter(lambda x: x.id == amenity_id, amenity_list))
        if my_res:
            return jsonify(my_res[0].to_dict())
        raise NotFound()
    amenity_list = list(map(lambda x: x.to_dict(), amenity_list))
    return jsonify(amenity_list)


def remove_amenity(amenity_id=None):
    '''Removes a amenity with the given id.
    '''
    amenity_list = storage.all(Amenity).values()
    my_res = list(filter(lambda x: x.id == amenity_id, amenity_list))
    if my_res:
        storage.delete(my_res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    '''Adds a new amenity.
    '''
    my_data = request.get_json()
    if type(my_data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in my_data:
        raise BadRequest(description='Missing name')
    the_amenity = Amenity(**my_data)
    the_amenity.save()
    return jsonify(the_amenity.to_dict()), 201


def update_amenity(amenity_id=None):
    '''Updates the amenity with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    amenity_list = storage.all(Amenity).values()
    my_res = list(filter(lambda x: x.id == amenity_id, amenity_list))
    if my_res:
        my_data = request.get_json()
        if type(my_data) is not dict:
            raise BadRequest(description='Not a JSON')
        pre_amenity = my_res[0]
        for key, value in my_data.items():
            if key not in xkeys:
                setattr(pre_amenity, key, value)
        pre_amenity.save()
        return jsonify(pre_amenity.to_dict()), 200
    raise NotFound()

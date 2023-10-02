#!/usr/bin/python3
'''Contains the places_amenities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE', 'POST']
)
def handle_places_amenities(place_id=None, amenity_id=None):
    '''The method handler for the places endpoint.
    '''
    handlers = {
        'GET': get_place_amenities,
        'DELETE': remove_place_amenity,
        'POST': add_place_amenity
    }
    if request.method in handlers:
        return handlers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_place_amenities(place_id=None, amenity_id=None):
    '''Gets the amenities of a place with the given id.
    '''
    if place_id:
        aplace = storage.get(Place, place_id)
        if aplace:
            all_amenities = list(map(lambda x: x.to_dict(), aplace.amenities))
            return jsonify(all_amenities)
    raise NotFound()


def remove_place_amenity(place_id=None, amenity_id=None):
    '''Removes an amenity with a given id from a place with a given id.
    '''
    if place_id and amenity_id:
        aplace = storage.get(Place, place_id)
        if not aplace:
            raise NotFound()
        myamenity = storage.get(Amenity, amenity_id)
        if not myamenity:
            raise NotFound()
        aplace_amenity_link = list(
            filter(lambda x: x.id == amenity_id, aplace.amenities)
        )
        if not aplace_amenity_link:
            raise NotFound()
        if storage_t == 'db':
            amenity_place_link = list(
                filter(lambda x: x.id == place_id, myamenity.place_amenities)
            )
            if not amenity_place_link:
                raise NotFound()
            aplace.amenities.remove(myamenity)
            aplace.save()
            return jsonify({}), 200
        else:
            all_amenity_idx = aplace.amenity_ids.index(amenity_id)
            aplace.amenity_ids.pop(all_amenity_idx)
            aplace.save()
            return jsonify({}), 200
    raise NotFound()


def add_place_amenity(place_id=None, amenity_id=None):
    '''Adds an amenity with a given id to a aplace with a given id.
    '''
    if place_id and amenity_id:
        aplace = storage.get(Place, place_id)
        if not aplace:
            raise NotFound()
        myamenity = storage.get(Amenity, amenity_id)
        if not myamenity:
            raise NotFound()
        if storage_t == 'db':
            aplace_amenity_link = list(
                filter(lambda x: x.id == amenity_id, aplace.amenities)
            )
            amenity_place_link = list(
                filter(lambda x: x.id == place_id, myamenity.place_amenities)
            )
            if amenity_place_link and aplace_amenity_link:
                res = myamenity.to_dict()
                del res['place_amenities']
                return jsonify(res), 200
            aplace.amenities.append(myamenity)
            aplace.save()
            res = myamenity.to_dict()
            del res['place_amenities']
            return jsonify(res), 201
        else:
            if amenity_id in aplace.amenity_ids:
                return jsonify(myamenity.to_dict()), 200
            aplace.amenity_ids.push(amenity_id)
            aplace.save()
            return jsonify(myamenity.to_dict()), 201
    raise NotFound()

#!/usr/bin/python3
'''Contains the users view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    '''Gets the user with the given id or all users.
    '''
    if user_id:
        my_user = storage.get(User, user_id)
        if my_user:
            obj = my_user.to_dict()
            if 'places' in obj:
                del obj['places']
            if 'reviews' in obj:
                del obj['reviews']
            return jsonify(obj)
        raise NotFound()
    all_my_users = storage.all(User).values()
    myusers = []
    for my_user in all_my_users:
        obj = my_user.to_dict()
        if 'places' in obj:
            del obj['places']
        if 'reviews' in obj:
            del obj['reviews']
        myusers.append(obj)
    return jsonify(myusers)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def remove_user(user_id):
    '''Removes a user with the given id.
    '''
    my_user = storage.get(User, user_id)
    if my_user:
        storage.delete(my_user)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/users', methods=['POST'])
def add_user():
    '''Adds a new user.
    '''
    mydata = {}
    try:
        mydata = request.get_json()
    except Exception:
        mydata = None
    if type(mydata) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in mydata:
        raise BadRequest(description='Missing email')
    if 'password' not in mydata:
        raise BadRequest(description='Missing password')
    my_user = User(**mydata)
    my_user.save()
    obj = my_user.to_dict()
    if 'places' in obj:
        del obj['places']
    if 'reviews' in obj:
        del obj['reviews']
    return jsonify(obj), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates the user with the given id.
    '''
    xkeys = ('id', 'email', 'created_at', 'updated_at')
    my_user = storage.get(User, user_id)
    if my_user:
        mydata = {}
        try:
            mydata = request.get_json()
        except Exception:
            mydata = None
        if type(mydata) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in mydata.items():
            if key not in xkeys:
                setattr(my_user, key, value)
        my_user.save()
        obj = my_user.to_dict()
        if 'places' in obj:
            del obj['places']
        if 'reviews' in obj:
            del obj['reviews']
        return jsonify(obj), 200
    raise NotFound()

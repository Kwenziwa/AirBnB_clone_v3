#!/usr/bin/python3
""" API endpoints for States """

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


def get_state_or_abort(state_id):
    """Retrieve a State object by ID or abort with 404 if not found"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    return my_state


def create_state(data):
    """Create a new state in the database."""
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return new_state


def validate_json():
    """Validate that the request data is in JSON format."""
    mydata = request.get_json()
    if not mydata:
        abort(400, "Not a JSON")
    return mydata


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    """Route for manipulating State objects"""

    if request.method == 'GET':
        # Get a list of all states
        states = storage.all(State)
        states_list = [state.to_dict() for state in states.values()]
        return jsonify(states_list)

    if request.method == 'POST':
        # Add a State to the list
        mydata = validate_json()
        if "name" not in mydata:
            abort(400, "Missing name")
        new_state = create_state(mydata)
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def state_with_id(state_id=None):
    """Route for manipulating a specific State object"""

    mystate = get_state_or_abort(state_id)

    if request.method == 'GET':
        # Get a specific state by id
        return jsonify(mystate.to_dict())

    if request.method == 'DELETE':
        # Delete a specific state by id
        storage.delete(mystate)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        # Update a specific state by id
        mydata = validate_json()
        for key, value in mydata.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(mystate, key, value)
        storage.save()
        return make_response(jsonify(mystate.to_dict()), 200)
    
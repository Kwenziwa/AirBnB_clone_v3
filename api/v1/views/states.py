from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State

# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

# Retrieves a State object: GET /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

# Deletes a State object: DELETE /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

# Creates a State: POST /api/v1/states
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

# Updates a State object: PUT /api/v1/states/<state_id>
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    # Ignore keys: id, created_at, and updated_at
    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

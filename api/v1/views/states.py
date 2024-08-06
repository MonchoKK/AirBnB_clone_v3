#!/usr/bin/python3
""" Defines a view for State objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    """ retrieves all State objects """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def get_state(state_id):
    """ retrieves State object (of ID), raising a 404 error if not found """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a State object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates a new State object
    Returns the new state and status code 201 """
    if not request.json:
        abort(400, description='Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(400, description='Missing name')
    # create new State
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ updates a State object
    Returns the updated state + status code 200 if successful,
    raising 4XX errors otherwise """
    if not request.json:
        abort(400, description='Not a JSON')
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)

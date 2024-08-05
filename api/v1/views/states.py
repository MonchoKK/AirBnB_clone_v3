#!/usr/bin/python3
""" Defines a view for State objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states')
def states():
    """ retrieves all State objects """
    states = storage.all(State).values()
    states_dicts = []
    for state in states:
        states_dicts.append(state.to_dict())
    return jsonify(states_dicts)


@app_views.route('/states/<state_id>')
def state(state_id):
    """ retrieves State object (of ID), raising a 404 error if
    not found """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ deletes a State object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    # get the object with id then delete it
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)  # obj is None


@app_views.route('/states', methods=['POST'])
def add_state():
    """ creates a new State object
    Returns the new state and status code 201 """
    # check that the request body is JSON
    if not request.json:
        return jsonify('Not a JSON'), 400
    state_info = request.get_json()  # returns a dict
    if 'name' not in state_info:
        abort(make_response(jsonify('Missing name'), 400))
    # create new State
    state = State(**state_info)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ updates a State object
    Returns the updated state + status code 200 if successful,
    raising 4XX errors  otherwise """
    # get the state to update
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        # abort(400)  # Not a JSON
        return jsonify('Not a JSON'), 400
    state_info = request.get_json()
    # update state (by updating/adding its attributes)
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in state_info.items():
        if key not in ignore:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

#!/usr/bin/python3
""" Defines a view for City objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities')
def state_cities(state_id):
    """ retrieves all the City objects of a State """
    # get the state, and if None, raise a 404
    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)  # state is None


@app_views.route('/cities/<city_id>')
def city(city_id):
    """ retrieves City object (of ID), raising a 404 error if
    not found """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ deletes a City object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    # get the object with id then delete it
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)  # obj is None


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """ creates a new City object
    Returns the new city and status code 201 """
    # check that the request body is JSON
    if not request.json:
        return jsonify('Not a JSON'), 400
    # check that state exists, else a 404 error
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_info = request.get_json()  # returns a dict
    if 'name' not in city_info:
        abort(make_response(jsonify('Missing name'), 400))
    # create new City
    city_info.update({'state_id': state_id})
    city = City(**city_info)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ updates a City object
    Returns the updated city + status code 200 if successful,
    raising 4XX errors  otherwise """
    # get the city to update
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        # abort(400)  # Not a JSON
        return jsonify('Not a JSON'), 400
    city_info = request.get_json()
    # update city (by updating/adding its attributes)
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in city_info.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

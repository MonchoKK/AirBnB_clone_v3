#!/usr/bin/python3
""" Defines a view for Amenity objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def amenities():
    """ retrieves all the Amenity objects """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>')
def amenity(amenity_id):
    """ retrieves Amenity object (of ID), raising a 404 error if
    not found """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ deletes a Amenity object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    # get the object with id then delete it
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)  # obj is None


@app_views.route('/amenities', methods=['POST'])
def add_amenity():
    """ creates a new Amenity object
    Returns the new amenity and status code 201 """
    # check that the request body is JSON
    if not request.json:
        return jsonify('Not a JSON'), 400
    amenity_info = request.get_json()  # returns a dict
    if 'name' not in amenity_info:
        abort(make_response(jsonify('Missing name'), 400))
    # create new Amenity
    amenity = Amenity(**amenity_info)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ updates a Amenity object
    Returns the updated amenity + status code 200 if successful,
    raising 4XX errors  otherwise """
    # get the amenity to update
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        return jsonify('Not a JSON'), 400
    amenity_info = request.get_json()
    # update amenity (by updating/adding its attributes)
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in amenity_info.items():
        if key not in ignore:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

#!/usr/bin/python3
""" Defines a view for Amenity objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
import os


store = os.getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities')
def place_amenities(place_id):
    """ retrieves all the Amenity objects of a Place """
    # get the place, and if None, raise a 404
    place = storage.get(Place, place_id)
    if place:
        if store == 'db':
            return jsonify([amenity.to_dict() for amenity in place.amenities])
        else:
            amenities = []
            for id in place.amenity_ids:
                amenities.append(storage.get(Amenity, id).to_dict())
            return jsonify(amenities)
    abort(404)  # place is None


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """ deletes a Amenity object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    # check that place (place_id) is valid
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    # get the object with id then delete it
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        # check that amenity is linked to place
        if store == 'db':
            place_amenities = place.amenities
        else:
            place_amenities = []
            for id in place.amenity_ids:
                place_amenities.append(storage.get(Amenity, id))
        for amenity_ in place_amenities:
            if amenity_.id == amenity.id:
                storage.delete(amenity)
                storage.save()
                return jsonify({}), 200  # linked, deleted
        abort(404)  # amenity not linked to place
    abort(404)  # amenity is None


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def add_place_amenity(place_id, amenity_id):
    """ links an Amenity object with a Place instance
    Returns the linked Amenity object and status code 201 """
    # check that place & amenity exist, else a 404 error
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    # link Amenity
    if store == 'db':
        # I need to append to place_amenities table...
        place_amenities = place.amenities
        for amenity_ in place_amenities:
            if amenity_.id == amenity_id:
                return jsonify(amenity.to_dict()), 200  # already linked
        # else, link (how??? -> append to the list and commit)
        place.amenities.append(amenity)
        place.save()
    else:
        place_amenities = place.amenity_ids
        if amenity.id in place_amenities:
            return jsonify(amenity.to_dict()), 200  # already linked
        # else, link (by appending to amenities)
        place.amenities = amenity
        place.save()
        # print('place_amenities: ', place.amenities)
    return jsonify(amenity.to_dict()), 201

#!/usr/bin/python3
""" Defines a view for Review objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews')
def place_reviews(place_id):
    """ retrieves all the Review objects of a Place """
    # get the place, and if None, raise a 404
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)  # place is None


@app_views.route('/reviews/<review_id>')
def review(review_id):
    """ retrieves Review object (of ID), raising a 404 error if
    not found """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ deletes a Review object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    # get the object with id then delete it
    obj = storage.get(Review, review_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)  # obj is None


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_review(place_id):
    """ creates a new Review object
    Returns the new review and status code 201 """
    # check that the request body is JSON
    if not request.json:
        return jsonify('Not a JSON'), 400
    # check that place exists, else a 404 error
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_info = request.get_json()  # returns a dict
    checks = ['user_id', 'text']  # link to user and have some text
    for check in checks:
        if check not in review_info:
            abort(make_response(jsonify('Missing {}'.format(check)), 400))
    # check that user (user_id) is valid
    user = storage.get(User, review_info['user_id'])
    if not user:
        abort(404)
    # create new Review
    review_info.update({'place_id': place_id})
    review = Review(**review_info)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ updates a Review object
    Returns the updated review + status code 200 if successful,
    raising 4XX errors  otherwise """
    # get the review to update
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        # abort(400)  # Not a JSON
        return jsonify('Not a JSON'), 400
    review_info = request.get_json()
    # update review (by updating/adding its attributes)
    ignore = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    for key, value in review_info.items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

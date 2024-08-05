#!/usr/bin/python3
""" Defines a view for User objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users')
def users():
    """ retrieves all the User objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>')
def user(user_id):
    """ retrieves User object (of ID), raising a 404 error if
    not found """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ deletes a User object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    # get the object with id then delete it
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)  # obj is None


@app_views.route('/users', methods=['POST'])
def add_user():
    """ creates a new User object
    Returns the new user and status code 201 """
    # check that the request body is JSON
    if not request.json:
        return jsonify('Not a JSON'), 400
    user_info = request.get_json()  # returns a dict
    checks = ['email', 'password']
    for check in checks:
        if check not in user_info:
            abort(make_response(jsonify('Missing {}'.format(check)), 400))
    # create new User
    user = User(**user_info)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ updates a User object
    Returns the updated user + status code 200 if successful,
    raising 4XX errors  otherwise """
    # get the user to update
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        return jsonify('Not a JSON'), 400
    user_info = request.get_json()
    # update user (by updating/adding its attributes)
    ignore = ['id', 'created_at', 'updated_at', 'email']
    for key, value in user_info.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

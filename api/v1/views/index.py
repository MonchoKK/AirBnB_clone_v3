#!/usr/bin/python3
""" Define app_views' routes? """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from models import storage


# first route /status on the object app_views
@app_views.route('/status')
def status():
    """ Returns a JSON "status": "OK" """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def objects_count():
    """ Retrieves the number of each objects by type """
    objs_count = {}
    objs_count['amenities'] = storage.count(Amenity)
    objs_count['cities'] = storage.count(City)
    objs_count['places'] = storage.count(Place)
    objs_count['states'] = storage.count(State)
    objs_count['reviews'] = storage.count(Review)
    objs_count['users'] = storage.count(User)
    return jsonify(objs_count)

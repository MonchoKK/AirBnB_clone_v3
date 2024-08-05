#!/usr/bin/python3
""" Define Blueprint """
from flask import Blueprint

# create a Blueprint
app_views = Blueprint('app_views', __name__)

# import all routes (for this Blueprint)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *

#!/usr/bin/python3
"""Contains all Blueprint for API"""
from flask import Blueprint

api_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

from api.v1.views.admin import *
from api.v1.views.image import *
from api.v1.views.user import *

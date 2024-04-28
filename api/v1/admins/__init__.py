#!/usr/bin/python3
"""Contains all Blueprint for API"""
from flask import Blueprint

api_admins = Blueprint('api_admins', __name__, url_prefix='/api/v1')

from api.v1.admins.admin import *

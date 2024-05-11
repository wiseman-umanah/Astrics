#!/usr/bin/python3
"""This module controls all functionality for user development"""
from flask import abort, jsonify, make_response, request
from backend.models.user import User
from backend.models import storage
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
	"""Returns all users object available"""
	list_user = []
	users = storage.all(User).values()
	if not users:
		abort(404)
	for user in users:
		list_user.append(user.to_dict())
	return jsonify(list_user)

@app_views.route('/users/sub', methods=['GET'], strict_slashes=False)
def get_sub_users():
	"""Returns all users object available"""
	list_user = []
	users = storage.all(User).values()
	if not users:
		abort(404)
	for user in users:
		temp = user.to_dict()
		if temp["subscribed"] == True:
			list_user.append(temp)
	return jsonify(list_user)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
	"""Adds a new user to database"""
	data = request.get_json()
	if not data:
		abort(404, description="Not a valid JSON")
	if "email" not in data:
		abort(404, description="Missing email")
	elif "password" not in data:
		abort(404, description="Missing password")
	elif "username" not in data:
		abort(404, description="Missing first_name")
	instance = User(**data)
	instance.save()
	return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users_id(user_id):
	"""Returns all users object available based on id"""
	list_user = []
	user = storage.get(User, user_id)
	if not user:
		abort(404)
	list_user.append(user.to_dict())
	return jsonify(list_user)

from flask import abort, jsonify, make_response, request
from backend.models.user import User
from backend.models import storage
from api.v1.views import api_views


@api_views.route('/users', method=['GET'], strict_slashes=False)
def get_users():
	"""Returns all users object available"""
	list_user = {}
	user = storage.all(User)
	if not user:
		abort(404)
	list_user["users"] = user
	return jsonify(list_user)

@api_views.route('/users/sub', method=['GET'], strict_slashes=False)
def get_sub_users():
	"""Returns all users object available"""
	list_user = {}
	user = storage.all(User)
	if not user:
		abort(404)
	subs = [i["subscribed"] == "True" for i in user]
	list_user["users"] = subs
	return jsonify(list_user)

@api_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
	"""Adds a new user to database"""
	data = request.get_json()
	if not data:
		abort(404, description="Not a valid JSON")
	if "email" not in data:
		abort(404, description="Missing email")
	elif "password" not in data:
		abort(404, description="Missing password")
	elif "first_name" not in data:
		abort(404, description="Missing first_name")
	elif "last_name" not in data:
		abort(404, description="Missing last_name")
	instance = User(**data)
	instance.save()
	return make_response(jsonify(instance.to_dict()), 201)

@api_views.route('/users/<user_id>', method=['GET'], strict_slashes=False)
def get_users_id(user_id):
	"""Returns all users object available based on id"""
	list_user = {}
	image = storage.get(User, user_id)
	if not image:
		abort(404)
	list_user["user"] = image
	return jsonify(list_user)

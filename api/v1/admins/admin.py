#!/usr/bin/python3
"""This module controls all admin functionality for the web app"""
from flask import make_response, jsonify, abort, request
from backend.models.image import Image
from backend.models.admin import Admin
from backend.models import storage
from api.v1.admins import app_admins
from backend.models.user import User

@app_admins.route('/admins', methods=['GET'], strict_slashes=False)
def get_admins():
	"""Returns a list of the admins of the app"""
	list_admin = []
	admin = storage.all(Admin).values()
	if not admin:
		abort(404)
	for i in admin:
		temp = i.to_dict()
		del temp["id"]
	list_admin.append(temp)
	return jsonify(list_admin)

@app_admins.route('/admins/<admin_id>', methods=['GET'], strict_slashes=False)
def get_admin_id(admin_id):
	"""Returns all users object available based on id"""
	list_admin = []
	admin = storage.get(Admin, admin_id)
	if not admin:
		abort(404)
	temp = admin.to_dict()
	del temp["id"]
	list_admin.append(temp)
	return jsonify(list_admin)

@app_admins.route('/image/<admin_id>', methods=['POST'], strict_slashes=False)
def add_image(admin_id):
	"""Adds a new user to database"""
	if not (storage.get(Admin, admin_id)):
		abort(404)
	data = request.get_json()
	if not data:
		abort(404, description="Not a valid JSON")
	if "image_url" not in data:
		abort(404, description="Missing image source")
	elif "image_title" not in data:
		abort(404, description="Missing image title")
	instance = Image(**data)
	instance.save()
	return make_response(jsonify(instance.to_dict()), 201)

@app_admins.route('/image/<admin_id>/<image_id>', methods=['DELETE'],
				 strict_slashes=False)
def delete_pic(admin_id, image_id):
	"""
	Deletes an Image Object
	"""
	if not (storage.get(Admin, admin_id)):
		abort(404)
	image = storage.get(Image, image_id)

	if not image:
		abort(404)

	storage.delete(image)
	storage.save()

	return make_response(jsonify({}), 200)

@app_admins.route('/user/<admin_id>/<user_id>', methods=['DELETE'],
				 strict_slashes=False)
def delete_user(admin_id, user_id):
	"""
	Deletes a User Object
	"""
	if not (storage.get(Admin, admin_id)):
		abort(404)
	user = storage.get(User, user_id)

	if not user:
		abort(404)

	storage.delete(user)
	storage.save()

	return make_response(jsonify({}), 200)

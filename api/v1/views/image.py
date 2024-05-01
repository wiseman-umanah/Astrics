#!/usr/bin/python3
"""This module controls all functionality for image development"""
from flask import abort, jsonify, make_response, request
from backend.models.image import Image
from backend.models import storage
from api.v1.views import app_views


@app_views.route('/images', methods=['GET'], strict_slashes=False)
def get_images():
	"""Returns all images available in database"""
	list_image = []
	images = storage.all(Image).values()
	if not images:
		abort(404)
	for image in images:
		list_image.append(image.to_dict())
	return jsonify(list_image)


@app_views.route('/images/<image_id>', methods=['GET'], strict_slashes=False)
def get_image_id(image_id):
	"""Retrieves an image object based on the id"""
	list_image = []
	image = storage.get(Image, image_id)
	if not image:
		abort(404)
	list_image.append(image.to_dict())
	return jsonify(list_image)

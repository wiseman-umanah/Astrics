from flask import abort, jsonify, make_response, request
from backend.models.image import Image
from backend.models import storage
from api.v1.views import api_views


@api_views.route('/images', method=['GET'], strict_slashes=False)
def get_images():
	"""Returns all images available in database"""
	list_image = {}
	image = storage.all(Image)
	if not image:
		abort(404)
	list_image["images"] = image
	return jsonify(list_image)


@api_views.route('/images/<image_id>', methods=['GET'], strict_slashes=False)
def get_image_id(image_id):
	"""Retrieves an image object based on the id"""
	list_image = {}
	image = storage.get(Image, image_id)
	if not image:
		abort(404)
	list_image["images"] = image
	return jsonify(list_image)

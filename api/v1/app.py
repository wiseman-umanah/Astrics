#!/usr/bin/python3
"""Flask app to control API"""
from backend.models import storage
from os import getenv
from dotenv import load_dotenv
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from api.v1.views import app_views
from api.v1.admins import app_admins

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)
app.register_blueprint(app_admins)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_db(error):
	"""Closes database"""
	storage.close()

@app.errorhandler(404)
def not_found(error):
	"""catches any 404 error"""
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
	host = getenv('HOST')
	app.run(host="0.0.0.0", port="5001", threaded=True)

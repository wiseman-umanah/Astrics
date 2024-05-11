#!/usr/bin/python3
""" Starts a Flash Web Application """
import uuid
from backend.models import storage
from backend.models.image import Image
from backend.models.admin import Admin
from backend.models.user import User
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user
from os import getenv
from dotenv import load_dotenv
from hashlib import md5


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = getenv('PWD')


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200), nullable=False, unique=True)
	email = db.Column(db.String(200), nullable=False, unique=True)
	password = db.Column(db.String(100), nullable=False)

db.init_app(app)

with app.app_context():
	db.create_all()

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.teardown_appcontext
def close_db(error):
	""" Remove the current SQLAlchemy Session """
	storage.close()


@app.route('/home', strict_slashes=False)
def astrics():
	images = storage.all(Image).values()
	images = sorted(images, key=lambda k: k.created_at)
	img = []

	for image in images:
		img.append(image.to_dict())

	return render_template('home.html',
						   images=img,
						   cache_id=uuid.uuid4())



@app.route('/about', strict_slashes=False)
def astrics_about():
	admins = storage.all(Admin).values()
	adm = []
	
	for i in admins:
		adm.append(i.to_dict())
	return render_template('about.html', admins = adm)
	

@app.route('/projects', strict_slashes=False)
def astrics_projects():
	return render_template('projects.html')


@app.route('/contact', strict_slashes=False)
def astrics_contact():
	return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def astrics_login():
	if request.method == "POST":
		email = Users.query.filter_by(
			email=request.form.get("email")).first()
		if email:
			if email.password == md5(request.form.get("password").encode()).hexdigest():
				login_user(email)
				return redirect(url_for("astrics"))
			else:
				return redirect(url_for('astrics_register'))
		else:
			return redirect(url_for('astrics_register'))
	return render_template('login-page.html')


@app.route('/', strict_slashes=False)
@app.route('/register', methods=["GET", "POST"], strict_slashes=False)
def astrics_register():
	if request.method == "POST":
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")

		# Check if user already exists
		existing_user = Users.query.filter((Users.username == username) | (Users.email == email)).first()
		if existing_user:
			return redirect(url_for('astrics_register'))


		# Create a new user instance
		password = md5(password.encode()).hexdigest()
		user = Users(username=username, email=email, password=password)
		
		#saving to grand database(mysql)
		data = {'username': username, 
				'email': email, 
				"password": password}
		instance = User(**data)
		instance.save()
		# Add to the database
		db.session.add(user)
		db.session.commit()

		return redirect(url_for("astrics"))
	return render_template("register.html")


if __name__ == "__main__":
	""" Main Function """
	app.run()

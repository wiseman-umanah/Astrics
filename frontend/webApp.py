#!/usr/bin/python3
"""Starts a Flask Web Application"""
import uuid
from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_user, logout_user
from os import getenv
from dotenv import load_dotenv
from backend.models import db, storage, User
from hashlib import md5
import os
import json


load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DB_LINK")
app.config['SECRET_KEY'] = getenv('PWD')

# Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'astrics_login'

@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)

@app.teardown_appcontext
def close_db(error):
    """Remove the current SQLAlchemy Session"""
    storage.close()

@app.route('/home', strict_slashes=False)
def astrics_home():
    # Load images from file.json
    img = load_data_from_file(r"frontend/tools/image.json")
    return render_template('home.html', images=img[::-1], cache_id=uuid.uuid4())

def load_data_from_file(filename):
    """Load images from file.json"""
    data = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    return data

@app.route('/about', strict_slashes=False)
def astrics_about():
    adm = load_data_from_file("frontend/tools/dev.json")
    print(adm)
    return render_template('about.html', admin=adm)

@app.route('/projects', strict_slashes=False)
def astrics_projects():
    pro = load_data_from_file(r"frontend/tools/projects.json")
    return render_template('projects.html', projects=pro)

@app.route('/contact', strict_slashes=False)
def astrics_contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def astrics_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = storage.get(User, email)
        print(user.password)
        if user and (user.password == md5((password).encode()).hexdigest()):
            login_user(user)
            return redirect(url_for("astrics_home"))
        return redirect(url_for('astrics_login'))  # Redirect to login if credentials are incorrect
    return render_template('login.html')

@app.route('/', strict_slashes=False)
def astrics():
    return render_template('landing-page.html')

@app.route('/register', methods=["GET", "POST"], strict_slashes=False)
def astrics_register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = storage.get(User, email)
        if existing_user:
            return redirect(url_for('astrics_login'))  # Redirect to registration if user exists

        hashed_password = md5(password.encode()).hexdigest()
        user = User(username=username, email=email, password=hashed_password)

        storage.new(user)
        storage.save()

        return redirect(url_for("astrics_home"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

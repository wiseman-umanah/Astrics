#!/usr/bin/python3
""" Starts a Flash Web Application """
import uuid
from backend.models import storage
from backend.models.image import Image
from flask import Flask, render_template


app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
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


if __name__ == "__main__":
    """ Main Function """
    app.run()

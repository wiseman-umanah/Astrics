#!/usr/bin/python3
from backend.models import storage
from backend.models.image import Image
import json
import os


def save_image_to_file(new_image):
    """Save a new image object to image.json"""
    new_image_dict = new_image.to_dict()

    # Read existing data from file if it exists
    if os.path.exists("frontend/tools/image.json"):
        with open("frontend/tools/image.json", "r") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Append the new image to the existing data
    existing_data.append(new_image_dict)

    # Write combined data back to file.json
    with open("frontend/tools/image.json", "w") as file:
        json.dump(existing_data, file, indent=4)

    return new_image_dict


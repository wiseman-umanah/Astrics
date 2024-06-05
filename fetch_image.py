#!/usr/bin/python3
"""
Fetches the new image from NASA API
and saves to database
"""
import schedule
import time
import requests
from os import getenv
from dotenv import load_dotenv
from backend.models.image import Image
from backend.sendmail import send_email
from backend.save_to_file import save_image_to_file

load_dotenv()

key = getenv("API_KEY")
link = getenv("NASA_LINK")
r = requests.get(f"{link}?api_key={key}")

def get_images_des(link=None):
	new_dict = {}
	if link.status_code != 200:
		return False
	response = r.json()
	if response == {}:
		return False
	new_dict["image_url"] = response["url"]
	new_dict["image_title"] = response["title"]
	new_dict["description"] = response["explanation"]
	instance = Image(**new_dict)
	print(instance.id)
	send_email(new_dict["image_url"])
	instance.save()
	save_image_to_file(instance)

schedule.every().day.at("06:30").do(lambda: get_images_des(r))

while True:
	schedule.run_pending()
	time.sleep(1)

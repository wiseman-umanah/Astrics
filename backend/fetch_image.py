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


load_dotenv()

key = getenv("API_KEY")
link = getenv("NASA_LINK")
print(key, link)
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
	# print(new_dict)
	instance = Image(**new_dict)
	# print(instance.id)
	instance.save()

schedule.every(24).hours.do(get_images_des(r))

while True:
	schedule.run_pending()
	time.sleep(1)

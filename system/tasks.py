# Handle expensive tasks 
import requests
from os import getenv
from . models import AstricsModel
from celery import shared_task
from utils.emails import (notify_admins,
						  notify_user_new_content)


@shared_task
def fetch_daily_content():
	try:
		api_key = getenv('API_KEY')
		url = getenv('NASA_LINK')
		params = {'api_key': api_key}
		response = requests.get(url, params=params)

		if response.status_code == 200:
			data = response.json()
			content, created = AstricsModel.objects.update_or_create(
				date = data['date'],
				defaults={
					'title': data['title'],
					'description': data.get('explanation', ""),
					'url': data.get('hdurl', data["url"]),
					'media_type': data['media_type'],
				}
			)
			if created:
				notify_user_new_content(content)
		else:
			raise Exception(f"Failed to fetch data from NASA API: {response.status_code}")
		
	except Exception as error:
		print(str(error))
		notify_admins(str(error))		


from django import template
from os import getenv


url = f'https://cloud.appwrite.io/v1/storage/buckets/{getenv("BUCKET_ID")}'
register = template.Library()


@register.filter
def get_pic_link(user, type=0):
	if type == 0:
		if user.profile.cover_pic:
			return f'{url}/files/{user.profile.cover_pic}/view?project={getenv("PROJECT_ID")}'
		return f'{url}/files/676f9e31001d36cc6d4d/view?project={getenv("PROJECT_ID")}'
	
	if user.profile.profile_pic:
		return f'{url}/files/{user.profile.profile_pic}/view?project={getenv("PROJECT_ID")}'
	else:
		return f'{url}/files/676bd2d3000e5e2003ae/view?project={getenv("PROJECT_ID")}'
	
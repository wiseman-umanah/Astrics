#!/usr/bin/python3
"""The image model"""
from backend.models.base_model import BaseModel
from backend.models import storage_type
from sqlalchemy import Column, String


class Image(BaseModel):
	"""Image Data Structure"""
	if storage_type == "db":
		image_url = Column(String(250), nullable=False)
		image_title = Column(String(250), nullable=False)
		description = Column(String(2000))
	else:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.image_url = ""
			self.image_title = ""
			self.description = ""

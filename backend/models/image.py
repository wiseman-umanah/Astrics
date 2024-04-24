#!/usr/bin/python3
"""The image model"""
from backend.models.base_model import BaseModel



class Image(BaseModel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.url = "https"
		self.title = "Map"
		self.description = "Hello World"

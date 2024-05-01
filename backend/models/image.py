#!/usr/bin/python3
"""The image model"""
from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Image(BaseModel, Base):
	"""Image Data Structure"""
	if getenv("STORAGE_MET") == "db":
		__tablename__ = "images"
		id = Column(String(60), primary_key=True)
		image_url = Column(String(250), nullable=False)
		image_title = Column(String(250), nullable=False)
		description = Column(String(2000))
		created_at = Column(DateTime, default=datetime.utcnow)
	else:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.image_url = ""
			self.image_title = ""
			self.description = ""

#!/usr/bin/python3
"""This module defines a class User"""
from backend.models.base_model import BaseModel, Base
from os import getenv 
from sqlalchemy import Column, String, Boolean, DateTime
from dotenv import load_dotenv
from datetime import datetime
from hashlib import md5


load_dotenv()


class User(BaseModel, Base):
	"""This class defines a user by various attributes"""
	if  getenv("STORAGE_MET") == "db":
		__tablename__ = "users"
		id = Column(String(60), primary_key=True)
		email = Column(String(200), nullable=False)
		password = Column(String(200), nullable=False)
		username = Column(String(100), nullable=False, unique=True)
		created_at = Column(DateTime, default=datetime.utcnow)
		subscribed = Column(Boolean, unique=False, default=True)
	else:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.email = ""
			self.password = ""
			self.first_name = ""
			self.last_name = ""
			self.subscribed = True


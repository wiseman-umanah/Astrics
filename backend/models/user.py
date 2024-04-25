#!/usr/bin/python3
"""This module defines a class User"""
from backend.models.base_model import BaseModel, Base
from backend.models import storage_type
from sqlalchemy import Column, String


class User(BaseModel, Base):
	"""This class defines a user by various attributes"""
	if storage_type == "db":
		__tablename__ = "users"
		email = Column(String(500), nullable=False)
		password = Column(String(30), nullable=False)
		first_name = Column(String(100), nullable=False)
		last_name = Column(String(100), nullable=False)
	else:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.email = ""
			self.password = ""
			self.first_name = ""
			self.last_name = ""


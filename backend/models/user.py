#!/usr/bin/python3
"""This module defines a class User"""
from backend.models.base_model import BaseModel


class User(BaseModel):
	"""This class defines a user by various attributes"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.email = ""
		self.password = ""
		self.first_name = ""
		self.last_name = ""


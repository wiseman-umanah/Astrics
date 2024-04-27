#!/usr/bin/python3
"""This module defines a class Admins"""
from backend.models.base_model import BaseModel, Base
from os import getenv 
from sqlalchemy import Column, String
from dotenv import load_dotenv


load_dotenv()


class Admin(BaseModel, Base):
	"""This class defines a user by various attributes"""
	if  getenv("STORAGE_MET") == "db":
		__tablename__ = "admins"
		id = Column(String(60), primary_key=True)
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


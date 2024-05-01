#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv
from dotenv import load_dotenv

load_dotenv()

time = "%Y-%m-%dT%H:%M:%S.%f"

if getenv("STORAGE_MET") == "db":
	Base = declarative_base()
else:
	Base = object

class BaseModel:
	"""A base class for all hbnb models"""
		
	def __init__(self, *args, **kwargs):
		"""Instatntiates a new model"""
		if kwargs:
			for key, value in kwargs.items():
				if key != "__class__":
					setattr(self, key, value)
			if kwargs.get("created_at", None) and type(self.created_at) is str:
				self.created_at = datetime.strptime(kwargs["created_at"], time)
			else:
				self.created_at = datetime.utcnow()
			if kwargs.get("updated_at", None) and type(self.updated_at) is str:
				self.updated_at = datetime.strptime(kwargs["updated_at"], time)
			else:
				self.updated_at = datetime.utcnow()
			if kwargs.get("id", None) is None:
				self.id = str(uuid.uuid4())
		else:
			self.id = str(uuid.uuid4())
			self.created_at = datetime.utcnow()
			self.updated_at = self.created_at

	def __str__(self):
		"""Returns a string representation of the instance"""
		cls = (str(type(self)).split('.')[-1]).split('\'')[0]
		return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

	def save(self):
		"""Updates updated_at with current time when instance is changed"""
		from backend.models import storage
		self.updated_at = datetime.now()
		storage.new(self)
		storage.save()

	def to_dict(self):
		"""Convert instance into dict format"""
		dictionary = {}
		dictionary.update(self.__dict__)
		dictionary.update({'__class__':
						  (str(type(self)).split('.')[-1]).split('\'')[0]})
		if "_sa_instance_state" in dictionary:
			del dictionary["_sa_instance_state"]
		if "password" in dictionary:
			del dictionary["password"]
		return dictionary

	def delete(self):
		"""Delete the current instance from the storage"""
		from models import storage
		storage.delete(self)

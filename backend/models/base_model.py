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

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and isinstance(self.created_at, str):
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            if kwargs.get("updated_at", None) and isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from backend.models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = (str(type(self)).split('.')[-1]).split('\'')[0]
        dictionary['created_at'] = self.created_at.strftime(time)
        dictionary['updated_at'] = self.updated_at.strftime(time)
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        from backend.models import storage
        storage.delete(self)

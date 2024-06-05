#!/usr/bin/python3
from backend.models.base_model import BaseModel, Base
from flask_login import UserMixin
from sqlalchemy import Column, String
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class User(BaseModel, Base, UserMixin):
    __tablename__ = 'users'
    
    username = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(2048), nullable=False)

    def __init__(self, *args, **kwargs):
        """Handle instantiation from kwargs"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Convert instance into dict format with specific exclusions"""
        dictionary = super().to_dict()
        # Example of customization: exclude password
        if 'password' in dictionary:
            del dictionary['password']
        return dictionary

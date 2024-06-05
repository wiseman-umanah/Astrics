#!/usr/bin/python3
from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Image(Base, BaseModel):
    __tablename__ = 'images'
    image_url = Column(String(250), nullable=False)
    image_title = Column(String(250), nullable=False)
    description = Column(String(2000))

#!/usr/bin/python3
from os import getenv
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from backend.models.engine.file_storage import FileStorage
from backend.models.engine.db_storage import DBStorage

load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Determine storage type
storage_type = getenv("STORAGE_MET")
if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()

# Load storage data
storage.reload()

# Import models here to avoid circular imports
from backend.models.user import User
from backend.models.image import Image

# Make the storage and models available at the package level
__all__ = ["db", "storage", "User", "Image"]

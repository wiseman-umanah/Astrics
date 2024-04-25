#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from backend.models.engine.file_storage import FileStorage
from backend.models.engine.db_storage import DBStorage
from os import getenv

storage_type = getenv("STORAGE_MET")
if storage_type == "db":
	storage = DBStorage()
else:
	storage = FileStorage()
storage.reload()

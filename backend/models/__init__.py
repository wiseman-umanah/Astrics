#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from backend.models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()

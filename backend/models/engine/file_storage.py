#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from backend.models.base_model import BaseModel
from backend.models.image import Image
from backend.models.user import User

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'data.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
            dum = {}
            for i in FileStorage.__objects.keys():
                if i.startswith(cls.__name__):
                    dum[i] = FileStorage.__objects[i]
            return (dum)

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
                    'BaseModel': BaseModel, 'Image': Image,
                    'User': User
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from list of instances"""
        if obj is not None:
            delIns = f"{obj.__class__.__name__}.{obj.id}"
            del FileStorage.__objects[delIns]
            self.save()

    def close(self):
        """method for deserializing the JSON file to objects"""
        self.reload()

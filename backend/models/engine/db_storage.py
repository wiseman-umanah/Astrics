#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from backend.models.base_model import Base
from backend.models.user import User
from backend.models.image import Image
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

classes = {"Image": Image, "User": User}

class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine(getenv("DB_LINK"))

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, email):
        """
        Returns the object based on the class name and its email, or
        None if not found
        """
        if cls not in classes.values():
            return None
        return self.__session.query(cls).filter_by(email=email).first()

    def count(self, cls=None):
        """Count the number of objects in storage"""
        count = 0
        if cls:
            count = self.__session.query(cls).count()
        else:
            for clas in classes.values():
                count += self.__session.query(clas).count()
        return count

#!/usr/bin/python3
""" module for implementation of the FileStorage class
    Filestorage handles serializes and deserializes JSON types
"""

import json
import os
from collections import OrderedDict
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "Amenity": Amenity,
        "City": City,
        "Review": Review,
        "State": State
        }
classes1 = [BaseModel, User, State, Amenity, Place, Review]


class FileStorage:
    """
    A class that serializes instances to a JSON file
    It's also used to deserialize JSON file to instances.
    """
    __file_path = "storage.json"
    __objs = {}

    def all(self):
        """  A function that returns a dictionary of all objects.
        """
        return (self.__objs)

    def new(self, obj):
        """
        sets and adds new object to the dict
            Args:
                obj: The new object
        Returns when there is no no new object
        """
        if obj is None or not any(isinstance(obj, x) for x in classes1):
            return

        else:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objs[key] = obj

    def save(self):
        """ Function is used to serialize saving the data """

        obj_data = OrderedDict()

        for key, val in self.__objects.items():
            obj_data[key] = val.to_dict()

        with open(type(self).__file_path, "w", encoding="utf-8") as file:
            json.dumps(obj_data, file)

    def reload(self):
        """
        Function deserializes JSON file if it exists
        Exception: returns when the JSON file does not exist(does nothing)
        """

        try:
            object_data = {}  # Initilizing an empty dic
            with open(self.__file_path, "r") as file:
                object_data = json.loads(file.read())

                for key, v in object_data.items():
                    obj = classes[v['__class__']](**v)
                    self.__objects[key] = obj
        except Exception:
            return

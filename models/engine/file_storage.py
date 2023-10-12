#!/usr/bin/python3
""" module for implementation of the FileStorage class
    Filestorage handles serialization and deserialization of JSON types
"""

import json
import os
from collections import OrderedDict


class FileStorage:
    """ class that serializes instances to a JSON,
        file and deserializes JSON file to instances.
    """
    __file_path = "storage.json"
    __objects = {}

    def all(self) -> dict:
        """ public instance method that returns the
            dictionary __objects.
        """
        return self.__objects

    def new(self, obj) -> None:
        """ public instance method that sets in __objects
            the obj with key <obj class name>.id.
            Args:
                obj: an Object
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = [BaseModel, User, State, Amenity, Place, Review]
        if obj is None or not any(isinstance(obj, x) for x in classes):
            return

        if hasattr(obj, "id"):
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self) -> None:
        """ public instance method that serializes __objects
            to the JSON file (path: __file_path).
        """

        object_data = OrderedDict()

        for key, val in self.__objects.items():
            object_data[key] = val.to_dict()

        with open(type(self).__file_path, "w+") as file:
            file.write("{}".format(json.dumps(object_data)))

    def reload(self) -> None:
        """ public instance method that deserializes a JSON
            file to __objects,(only if the JSON file (__file_path) exists;
            otherwise, do nothing. If the file doesn’t exist,
            no exception should be raised).
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        if not os.path.exists(self.__file_path):
            return

        classes = {"BaseModel": BaseModel, "User": User,
                   "Place": Place, "Amenity": Amenity,
                   "City": City, "Review": Review, "State": State}

        jdata = {}
        with open(self.__file_path, "r") as file:
            jdata = json.loads(file.read())

        for key, val in jdata.items():
            obj = classes[val['__class__']](**val)
            self.__objects[key] = obj

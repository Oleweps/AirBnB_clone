#!/usr/bin/python3
"""
This module has Basemodel class that defines attributes and methods of
subsequent classes
"""


import datetime
from uuid import uuid4
from models import storage


class BaseModel:
    """
    The Basemodel class that has attributes to be inherited by
    child classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Used to initalize class BaseModel
        Args:
            args: list of arguments.
            kwargs: a dictionary of keyworded arguments.
        """
        if len(kwargs) > 0:
            attributes = self.__dict__

            for key, v in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    attributes[key] = self.__to_datetime(v)
                else:
                    attributes[key] = v
        else:
            self.id = str(uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            storage.new(self)

    def __str__(self):
        """
        Returns a string respresentation of the class BaseModel.
        """
        i = "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)
        return (i)

    def save(self):
        """
        Updates public instance updated_at with current datetime
        """

        self.updated_at = datetime.datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns all keys/values of __dict__(dictionary)
        """
        dic = self.__dict__
        dic = dict(self.__dict__)
        dic["created_at"] = self.convert_to_string(dic["created_at"])
        dic["updated_at"] = self.convert_to_string(dic["updated_at"])
        dic["__class__"] = self.__class__.__name__

        return (dic)

    def convert_to_string(self, date_obj: datetime):
        """
        Converts and returns datetime obj to string in ISO format.
            Args:
                date_obj: The datetime object.
        """

        return (date_obj.isoformat())

    def convert_to_datetime(self, date_str: str):
        """
        Converts date string to datetime object.
            Args:
                date_string: the date string.
            Return:
                  It returns the datetime object from string.
        """

        return (datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f"))

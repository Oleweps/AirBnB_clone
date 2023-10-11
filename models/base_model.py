#!/usr/bin/python3
""" Base model class module
"""

from uuid import uuid4
from datetime import datetime

from models import storage

CURRENT_DATE = datetime.now()


class BaseModel:
    """ BaseModel that defines all common,
        attributes/methods for other classes.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ method to initalize class BaseModel
            Args:
                args: a list of positional arguments.
                kwargs: a dict of keyword arguments.
        """
        if len(kwargs) > 0:  # if kwargs is not empty
            attrs = self.__dict__

            for key, val in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "updated_at" or key == "created_at":
                    attrs[key] = self.__to_datetime(val)
                else:
                    attrs[key] = val
        else:
            self.id = str(uuid4())
            self.created_at = CURRENT_DATE
            self.updated_at = CURRENT_DATE
            storage.new(self)

    def __str__(self) -> str:
        """ get string respresentation of class BaseModel.
            Return:
                  string represtation of BaseModel.
        """
        class_name = self.__class__.__name__
        return "[{0}] ({1}) {2}".format(class_name, self.id, self.__dict__)

    def save(self) -> None:
        """ update public instance updated_at
        """

        self.updated_at = CURRENT_DATE  # update updated_at attribute
        storage.save()

    def to_dict(self) -> dict:
        """ get and return all keys/values of __dict__
           Return:
                 a dictionary containing all,
                 keys/values of __dict__ of the instance.
        """
        base_dict = self.__dict__
        base_dict = dict(self.__dict__)
        base_dict["created_at"] = self.__to_string(base_dict["created_at"])
        base_dict["updated_at"] = self.__to_string(base_dict["updated_at"])
        base_dict["__class__"] = self.__class__.__name__

        return base_dict

    def __to_string(self, date: datetime) -> str:
        """ convert datetime object to string in ISO format
            Return:
                  string represetation of datetime object in ISO format.
        """
        return date.isoformat()

    def __to_string(self, date_obj: datetime) -> str:
        """ convert datetime object to string in ISO format.
            Args:
                date_obj: datetime object.
            Return:
                  string represetation of datetime object in ISO format.
        """

        return date_obj.isoformat()

    def __to_datetime(self, date_string: str) -> datetime:
        """ convert string represantation of date to datetime object.
            Args:
                date_string: datetime string.
            Return:
                  datetime object from string.
        """

        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")

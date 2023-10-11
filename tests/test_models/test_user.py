#!/usr/bin/python3
""" module to test User class.
"""

import unittest
from datetime import datetime, timedelta
import os

from models import storage
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """ class TestUser to test User class.
    """
    def setUp(self):
        """ initialize class
        """
        self.user_no_kwargs = None
        self.all_objs = storage.all()
        self.size = len(self.all_objs)  # number of items in storage
        self.user_with_kwargs = None
        self.yesterday = datetime.now() - timedelta(days=1)

    def test_all_attributes_are_present(self):
        """ test all attributes are present
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        self.assertTrue(hasattr(self.user_no_kwargs, "id"))
        self.assertTrue(hasattr(self.user_no_kwargs, "email"))
        self.assertTrue(hasattr(self.user_no_kwargs, "password"))
        self.assertTrue(hasattr(self.user_no_kwargs, "first_name"))
        self.assertTrue(hasattr(self.user_no_kwargs, "last_name"))
        self.assertTrue(hasattr(self.user_no_kwargs, "created_at"))
        self.assertTrue(hasattr(self.user_no_kwargs, "updated_at"))

    def test_attributes_data_types(self):
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()

        self.assertIsInstance(self.user_no_kwargs.id, str)
        self.assertIsInstance(self.user_no_kwargs.email, str)
        self.assertIsInstance(self.user_no_kwargs.password, str)
        self.assertIsInstance(self.user_no_kwargs.first_name, str)
        self.assertIsInstance(self.user_no_kwargs.last_name, str)
        self.assertIsInstance(self.user_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.user_no_kwargs.updated_at, datetime)

    def test_add_new_attributes(self):
        self.user_no_kwargs = User()
        self.user_no_kwargs.city = "test.com"
        self.user_no_kwargs.save()

        self.assertTrue(hasattr(self.user_no_kwargs, "city"))

    def test_user_subclass_of_base_model(self):
        """ check if User inherits from BaseModel
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        assert issubclass(type(self.user_no_kwargs), (BaseModel,))

    def test_create_user_no_kwargs(self):
        """ create User with no **kwargs
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        self.user_no_kwargs.updated_at = self.yesterday
        to_dict = self.user_no_kwargs.to_dict()

        self.assertIsInstance(self.user_no_kwargs, User)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_create_user_with_kwargs(self):
        """ create User with **kwargs
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        self.user_with_kwargs = User(**self.user_no_kwargs.to_dict())
        self.user_with_kwargs.updated_at = self.yesterday
        to_dict = self.user_with_kwargs.to_dict()

        self.assertIsInstance(self.user_with_kwargs, User)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_id_is_string(self):
        """ check if id attribute contains a string.
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        self.assertIsInstance(self.user_no_kwargs.id, str)

    def test_dates_are_datetime_object(self):
        """ check if all dates in User object are datetime objects
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        self.assertIsInstance(self.user_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.user_no_kwargs.updated_at, datetime)

    def test_save_method(self):
        """ test save method in User
        """
        new_size = self.size
        user = User()
        user.save()

        self.all_objs = storage.all()
        self.size = len(self.all_objs)

        self.assertIsInstance(self.all_objs, dict)
        self.assertGreater(self.size, new_size)

    def test_update_at_is_modified_on_save(self):
        self.user_no_kwargs = User()
        self.user_no_kwargs.updated_at = self.yesterday
        previous_date = self.user_no_kwargs.updated_at
        self.user_no_kwargs.save()

        self.assertNotEqual(previous_date, self.user_no_kwargs.updated_at)

    def test_to_dict_method(self):
        """ tests on to_dict method.
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        new_dict = self.user_no_kwargs.to_dict()
        self.assertIsInstance(new_dict, dict)
        # check of all the dates objects have been converted to string format
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertIsNotNone(new_dict["__class__"])
        self.assertIsInstance(new_dict["__class__"], str)

    def test_user_model_to_string(self):
        """ test if User class can be represented as a string
        """
        self.user_no_kwargs = User()
        self.user_no_kwargs.save()
        self.assertIsInstance(str(self.user_no_kwargs), str)

    def tearDown(self):
        """ teardown function"""
        self.user_no_kwargs = None
        self.user_with_kwargs = None
        self.yesterday = None
        self.all_objs = None
        self.size = 0
        os.remove("storage.json")


if __name__ == "__main__":
    unittest.main()

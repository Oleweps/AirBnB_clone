#!/usr/bin/python3
""" module to test City class
"""

import unittest
import os

from datetime import datetime, timedelta
from models import storage
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    """ class TestCity to test City class.
    """
    def setUp(self):
        """ initialize class
        """
        self.city_no_kwargs = None
        self.city_with_kwargs = None
        self.yesterday = datetime.now() - timedelta(days=1)
        self.all_objs = storage.all()
        self.size = len(self.all_objs)  # number of items in storage

    def test_all_attributes_are_present(self):
        """ test all attributes are present
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        self.assertTrue(hasattr(self.city_no_kwargs, "id"))
        self.assertTrue(hasattr(self.city_no_kwargs, "state_id"))
        self.assertTrue(hasattr(self.city_no_kwargs, "name"))
        self.assertTrue(hasattr(self.city_no_kwargs, "created_at"))
        self.assertTrue(hasattr(self.city_no_kwargs, "updated_at"))

    def test_all_attributes_data_types(self):

        self.city_no_kwargs = City()
        self.city_no_kwargs.save()

        self.assertIsInstance(self.city_no_kwargs.id, str)
        self.assertIsInstance(self.city_no_kwargs.state_id, str)
        self.assertIsInstance(self.city_no_kwargs.name, str)
        self.assertIsInstance(self.city_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.city_no_kwargs.updated_at, datetime)

    def test_add_new_attribute(self):

        self.city_no_kwargs = City()
        self.city_no_kwargs.test = "cool"
        self.city_no_kwargs.save()

        self.assertTrue(hasattr(self.city_no_kwargs, "test"))

    def test_city_subclass_of_base_model(self):
        """ check if City inherits from BaseModel
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        assert issubclass(type(self.city_no_kwargs), (BaseModel,))

    def test_save_city(self):
        """ test save method
        """
        new_size = self.size
        city = City()
        city.save()

        self.all_objs = storage.all()
        self.size = len(self.all_objs)

        self.assertIsInstance(self.all_objs, dict)
        self.assertGreater(self.size, new_size)

    def test_update_at_is_modified_on_save(self):
        self.city_no_kwargs = City()
        self.city_no_kwargs.updated_at = self.yesterday
        previous_date = self.city_no_kwargs.updated_at
        self.city_no_kwargs.save()

        self.assertNotEqual(previous_date, self.city_no_kwargs.updated_at)

    def test_create_city_no_kwargs(self):
        """ create City with no **kwargs
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        self.city_no_kwargs.updated_at = self.yesterday
        to_dict = self.city_no_kwargs.to_dict()

        self.assertIsInstance(self.city_no_kwargs, City)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_create_city_with_kwargs(self):
        """ create City with **kwargs
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        self.city_with_kwargs = City(**self.city_no_kwargs.to_dict())
        self.city_with_kwargs.updated_at = self.yesterday
        to_dict = self.city_with_kwargs.to_dict()

        self.assertIsInstance(self.city_with_kwargs, City)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_id_is_string(self):
        """ check if id attribute contains a string.
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        self.assertIsInstance(self.city_no_kwargs.id, str)

    def test_dates_are_datetime_object(self):
        """ check if all dates in BaseModel object are datetime objects
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        self.assertIsInstance(self.city_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.city_no_kwargs.updated_at, datetime)

    def test_to_dict_method(self):
        """ tests on to_dict method.
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        new_dict = self.city_no_kwargs.to_dict()
        self.assertIsInstance(new_dict, dict)
        # check of all the dates objects have been converted to string format
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertIsNotNone(new_dict["__class__"])
        self.assertIsInstance(new_dict["__class__"], str)

    def test_city_to_string(self):
        """ test if City can be represented as a string
        """
        self.city_no_kwargs = City()
        self.city_no_kwargs.save()
        self.assertIsInstance(str(self.city_no_kwargs), str)

    def tearDown(self):
        """ teardown function """
        self.city_no_kwargs = None
        self.city_with_kwargs = None
        self.yesterday = None
        self.all_objects = None
        self.size = 0
        if os.path.exists("storage.json"):
            os.remove("storage.json")


if __name__ == "__main__":
    unittest.main()

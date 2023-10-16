#!/usr/bin/python3
""" module to test Amenity class
"""

import unittest
from datetime import datetime, timedelta
import os

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """ class TestAmenity to run tests on Amenity
    """
    def setUp(self):
        """ initialize class
        """
        self.amenity_no_kwargs = None
        self.amenity_with_kwargs = None
        self.yesterday = datetime.now() - timedelta(days=1)
        self.all_objs = storage.all()
        self.size = len(self.all_objs)  # number of items in storage

    def test_all_attributes_are_available(self):
        """ test all attributes are present
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()
        self.assertTrue(hasattr(self.amenity_no_kwargs, "id"))
        self.assertTrue(hasattr(self.amenity_no_kwargs, "name"))
        self.assertTrue(hasattr(self.amenity_no_kwargs, "created_at"))
        self.assertTrue(hasattr(self.amenity_no_kwargs, "updated_at"))

    def test_attributes_data_types(self):
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()

        self.assertIsInstance(self.amenity_no_kwargs.id, str)
        self.assertIsInstance(self.amenity_no_kwargs.name, str)
        self.assertIsInstance(self.amenity_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.amenity_no_kwargs.updated_at, datetime)

    def test_add_new_attributes(self):
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.city = "test.com"
        self.amenity_no_kwargs.save()

        self.assertTrue(hasattr(self.amenity_no_kwargs, "city"))

    def test_amenity_subclass_of_base_model(self):
        """ check if Amenity inherits from BaseModel
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()

        assert issubclass(type(self.amenity_no_kwargs), (BaseModel,))

    def test_save_amenity(self):
        """ test save method Amenity
        """
        new_size = self.size
        amenity = Amenity()
        amenity.save()

        self.all_objs = storage.all()
        self.size = len(self.all_objs)

        self.assertIsInstance(self.all_objs, dict)
        self.assertGreater(self.size, new_size)

    def test_updated_at_is_modified_after_save(self):

        amenity = Amenity()
        amenity.updated_at = self.yesterday
        previous_date = amenity.updated_at
        amenity.save()

        self.assertNotEqual(previous_date, amenity.updated_at)

    def test_create_amenity_no_kwargs(self):
        """ create Amenity with no **kwargs
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()
        self.amenity_no_kwargs.updated_at = self.yesterday
        to_dict = self.amenity_no_kwargs.to_dict()

        self.assertIsInstance(self.amenity_no_kwargs, Amenity)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_create_amenity_with_kwargs(self):
        """ create Amenity with **kwargs
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()
        self.amenity_with_kwargs = Amenity(**self.amenity_no_kwargs.to_dict())
        self.amenity_with_kwargs.updated_at = self.yesterday
        to_dict = self.amenity_with_kwargs.to_dict()

        self.assertIsInstance(self.amenity_with_kwargs, Amenity)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_id_is_string(self):
        """ check if id attribute contains a string.
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()
        self.assertIsInstance(self.amenity_no_kwargs.id, str)

    def test_dates_are_datetime_object(self):
        """ check if all dates in Amenity object are datetime objects
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()
        self.assertIsInstance(self.amenity_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.amenity_no_kwargs.updated_at, datetime)

    def test_to_dict_method(self):
        """ tests on to_dict method.
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()
        new_dict = self.amenity_no_kwargs.to_dict()

        self.assertIsInstance(new_dict, dict)
        # check of all the dates objects have been converted to string format
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertIsNotNone(new_dict["__class__"])
        self.assertIsInstance(new_dict["__class__"], str)

    def test_amenity_to_string(self):
        """ test Amenity can be represented as a string
        """
        self.amenity_no_kwargs = Amenity()
        self.amenity_no_kwargs.save()
        self.assertIsInstance(str(self.amenity_no_kwargs), str)

    def tearDown(self):
        """ teardown function """
        self.amenity_no_kwargs = None
        self.amenity_with_kwargs = None
        self.yesterday = None
        self.all_objects = None
        self.size = 0
        if os.path.exists("storage"):
            os.remove("storage.json")


if __name__ == "__main__":
    unittest.main()

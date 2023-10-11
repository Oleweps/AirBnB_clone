#!/usr/bin/python3
""" module to test FileStorage class.
"""

import unittest
from datetime import datetime, timedelta
import os

from models import storage
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """ Class TestPlace to test Place class.
    """
    def setUp(self):
        """ initialize class
        """
        self.place_no_kwargs = None
        self.place_with_kwargs = None
        self.yesterday = datetime.now() - timedelta(days=1)
        self.all_objs = storage.all()
        self.size = len(self.all_objs)  # number of items in storage

    def test_all_attributes_are_present(self):
        """ test all attributes are present
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        self.assertTrue(hasattr(self.place_no_kwargs, "id"))
        self.assertTrue(hasattr(self.place_no_kwargs, "city_id"))
        self.assertTrue(hasattr(self.place_no_kwargs, "user_id"))
        self.assertTrue(hasattr(self.place_no_kwargs, "name"))
        self.assertTrue(hasattr(self.place_no_kwargs, "description"))
        self.assertTrue(hasattr(self.place_no_kwargs, "number_rooms"))
        self.assertTrue(hasattr(self.place_no_kwargs, "number_bathrooms"))
        self.assertTrue(hasattr(self.place_no_kwargs, "max_guest"))
        self.assertTrue(hasattr(self.place_no_kwargs, "price_by_night"))
        self.assertTrue(hasattr(self.place_no_kwargs, "latitude"))
        self.assertTrue(hasattr(self.place_no_kwargs, "longitude"))
        self.assertTrue(hasattr(self.place_no_kwargs, "amenity_ids"))
        self.assertTrue(hasattr(self.place_no_kwargs, "created_at"))
        self.assertTrue(hasattr(self.place_no_kwargs, "updated_at"))

    def test_all_attributes_data_types(self):

        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        self.assertIsInstance(self.place_no_kwargs.id, str)
        self.assertIsInstance(self.place_no_kwargs.city_id, str)
        self.assertIsInstance(self.place_no_kwargs.user_id, str)
        self.assertIsInstance(self.place_no_kwargs.name, str)
        self.assertIsInstance(self.place_no_kwargs.description, str)
        self.assertIsInstance(self.place_no_kwargs.number_rooms, int)
        self.assertIsInstance(self.place_no_kwargs.number_bathrooms, int)
        self.assertIsInstance(self.place_no_kwargs.max_guest, int)
        self.assertIsInstance(self.place_no_kwargs.price_by_night, int)
        self.assertIsInstance(self.place_no_kwargs.latitude, float)
        self.assertIsInstance(self.place_no_kwargs.longitude, float)
        self.assertIsInstance(self.place_no_kwargs.amenity_ids, list)
        self.assertIsInstance(self.place_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.place_no_kwargs.updated_at, datetime)

    def test_add_new_attribute(self):
        self.place_no_kwargs = Place()
        self.place_no_kwargs.test = "cool"
        self.place_no_kwargs.save()

        self.assertTrue(hasattr(self.place_no_kwargs, "test"))

    def test_place_subclass_of_base_model(self):
        """ check if Place inherits from BaseModel
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        assert issubclass(type(self.place_no_kwargs), (BaseModel,))

    def test_save_place(self):
        """ test save method Place
        """
        new_size = self.size
        place = Place()
        place.save()
        self.all_objs = storage.all()
        self.size = len(self.all_objs)

        self.assertIsInstance(self.all_objs, dict)
        self.assertGreater(self.size, new_size)

    def test_update_at_is_modified_on_save(self):
        self.place_no_kwargs = Place()
        self.place_no_kwargs.updated_at = self.yesterday
        previous_date = self.place_no_kwargs.updated_at
        self.place_no_kwargs.save()

        self.assertNotEqual(previous_date, self.place_no_kwargs.updated_at)

    def test_create_place_no_kwargs(self):
        """ create Place with no **kwargs
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        self.place_no_kwargs.updated_at = self.yesterday
        to_dict = self.place_no_kwargs.to_dict()

        self.assertIsInstance(self.place_no_kwargs, Place)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_create_place_with_kwargs(self):
        """ create Place with **kwargs
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        self.place_with_kwargs = Place(**self.place_no_kwargs.to_dict())
        self.place_with_kwargs.updated_at = self.yesterday
        to_dict = self.place_with_kwargs.to_dict()

        self.assertIsInstance(self.place_with_kwargs, BaseModel)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_id_is_string(self):
        """ check if id attribute contains a string.
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        self.assertIsInstance(self.place_no_kwargs.id, str)

    def test_dates_are_datetime_object(self):
        """ check if all dates in Place object are datetime objects
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        self.assertIsInstance(self.place_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.place_no_kwargs.updated_at, datetime)

    def test_to_dict_method(self):
        """ tests on to_dict method.
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        new_dict = self.place_no_kwargs.to_dict()
        self.assertIsInstance(new_dict, dict)
        # check of all the dates objects have been converted to string format
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertIsNotNone(new_dict["__class__"])
        self.assertIsInstance(new_dict["__class__"], str)

    def test_place_to_string(self):
        """ test if Place can be represented as a string
        """
        self.place_no_kwargs = Place()
        self.place_no_kwargs.save()
        self.assertIsInstance(str(self.place_no_kwargs), str)

    def tearDown(self):
        """ teardown function """
        self.base_no_kwargs = None
        self.base_with_kwargs = None
        self.yesterday = None
        self.all_objects = None
        self.size = 0
        if os.path.exists("storage.json"):
            os.remove("storage.json")


if __name__ == "__main__":
    unittest.main()

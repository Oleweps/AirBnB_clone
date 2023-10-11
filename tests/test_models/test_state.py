#!/usr/bin/python3
""" State class test module
"""

import unittest
from datetime import datetime, timedelta
import os

from models import storage
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """ class TestState
    """
    def setUp(self):
        """ initialize class
        """
        self.state_no_kwargs = None
        self.all_objs = storage.all()
        self.size = len(self.all_objs)  # number of items in storage
        self.state_with_kwargs = None
        self.yesterday = datetime.now() - timedelta(days=1)

    def test_all_attributes_are_present(self):
        """ test all attributes are present
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        self.assertTrue(hasattr(self.state_no_kwargs, "id"))
        self.assertTrue(hasattr(self.state_no_kwargs, "name"))
        self.assertTrue(hasattr(self.state_no_kwargs, "created_at"))
        self.assertTrue(hasattr(self.state_no_kwargs, "updated_at"))

    def test_all__attributes_data_type(self):
        """ test the datattypes of attributes """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()

        self.assertIsInstance(self.state_no_kwargs.id, str)
        self.assertIsInstance(self.state_no_kwargs.name, str)
        self.assertIsInstance(self.state_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.state_no_kwargs.updated_at, datetime)

    def test_add_new_attributes(self):
        self.state_no_kwargs = State()
        self.state_no_kwargs.email = "test.com"
        self.state_no_kwargs.save()

        self.assertTrue(hasattr(self.state_no_kwargs, "email"))

    def test_state_subclass_of_base_model(self):
        """ check if State inherits from BaseModel
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        assert issubclass(type(self.state_no_kwargs), (BaseModel,))

    def test_save_state(self):
        """ test save State method
        """
        new_size = self.size
        state = State()
        state.save()
        self.all_objs = storage.all()
        self.size = len(self.all_objs)

        self.assertIsInstance(self.all_objs, dict)
        self.assertGreater(self.size, new_size)

    def test_update_at_is_modified_on_save(self):
        state = State()
        state.updated_at = self.yesterday
        previous_date = state.updated_at
        state.save()

        self.assertNotEqual(previous_date, state.updated_at)

    def test_create_state_no_kwargs(self):
        """ create State with no **kwargs
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        self.state_no_kwargs.updated_at = self.yesterday
        to_dict = self.state_no_kwargs.to_dict()

        self.assertIsInstance(self.state_no_kwargs, State)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_create_state_with_kwargs(self):
        """ create State with **kwargs
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        self.state_with_kwargs = State(**self.state_no_kwargs.to_dict())
        self.state_with_kwargs.updated_at = self.yesterday
        to_dict = self.state_with_kwargs.to_dict()

        self.assertIsInstance(self.state_with_kwargs, State)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_id_is_string(self):
        """ check if id attribute contains a string.
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        self.assertIsInstance(self.state_no_kwargs.id, str)

    def test_dates_are_datetime_object(self):
        """ check if all dates in State object are datetime objects
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        self.assertIsInstance(self.state_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.state_no_kwargs.updated_at, datetime)

    def test_to_dict_method(self):
        """ tests on to_dict method.
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        new_dict = self.state_no_kwargs.to_dict()
        self.assertIsInstance(new_dict, dict)
        # check of all the dates objects have been converted to string format
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertIsNotNone(new_dict["__class__"])
        self.assertIsInstance(new_dict["__class__"], str)

    def test_base_model_to_string(self):
        """ test if State class can be represented as a string
        """
        self.state_no_kwargs = State()
        self.state_no_kwargs.save()
        self.assertIsInstance(str(self.state_no_kwargs), str)

    def tearDown(self):
        """ teardown function """
        self.all_objects = None
        self.size = 0
        self.state_no_kwargs = None
        self.state_with_kwargs = None
        self.yesterday = None
        os.remove("storage.json")


if __name__ == "__main__":
    unittest.main()

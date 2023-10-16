#!/usr/bin/python3
""" class TEST_BASE_MODEL module
"""

from models.base_model import BaseModel

import unittest
from datetime import datetime, timedelta


class TestBaseModel(unittest.TestCase):
    """ Class to test BaseModel with no **kwargs
    """
    def setUp(self):
        """ initialize class
        """
        self.base_no_kwargs = BaseModel()
        self.base_with_kwargs = None
        self.yesterday = datetime.now() - timedelta(days=1)
        self.base_no_kwargs.updated_at = self.yesterday

    def test_create_base_model_no_kwargs(self):
        """ create BaseModel with no **kwargs
        """
        self.base_no_kwargs.updated_at = self.yesterday
        to_dict = self.base_no_kwargs.to_dict()

        self.assertIsInstance(self.base_no_kwargs, BaseModel)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_create_base_model_with_kwargs(self):
        """ create BaseModel with **kwargs
        """
        self.base_with_kwargs = BaseModel(**self.base_no_kwargs.to_dict())
        self.base_with_kwargs.updated_at = self.yesterday
        to_dict = self.base_with_kwargs.to_dict()

        self.assertIsInstance(self.base_with_kwargs, BaseModel)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_all_attributes_are_present(self):
        """ check if all BaseModel attributes are present..
        """

        self.assertTrue(hasattr(self.base_no_kwargs, "id"))
        self.assertTrue(hasattr(self.base_no_kwargs, "created_at"))
        self.assertTrue(hasattr(self.base_no_kwargs, "updated_at"))

    def test_all_attributes_data_types(self):

        self.base_no_kwargs = BaseModel()
        self.base_no_kwargs.save()
        self.assertIsInstance(self.base_no_kwargs.id, str)
        self.assertIsInstance(self.base_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.base_no_kwargs.created_at, datetime)

    def test_add_new_attribute(self):

        self.base_no_kwargs = BaseModel()
        self.base_no_kwargs.test = "cool"
        self.base_no_kwargs.save()

        self.assertTrue(hasattr(self.base_no_kwargs, "test"))

    def test_id_is_string(self):
        """ check if id attribute contains a string.
        """
        self.assertIsInstance(self.base_no_kwargs.id, str)

    def test_dates_are_datetime_object(self):
        """ check if all dates in BaseModel object are datetime objects
        """
        self.assertIsInstance(self.base_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.base_no_kwargs.updated_at, datetime)

    def test_save_method(self):
        """ test save method in BaseModel
        """
        previous_date = self.base_no_kwargs.updated_at
        self.base_no_kwargs.save()

        self.assertNotEqual(previous_date, self.base_no_kwargs.updated_at)

    def test_update_at_is_modified_on_save(self):
        self.base_no_kwargs = BaseModel()
        self.base_no_kwargs.updated_at = self.yesterday
        previous_date = self.base_no_kwargs.updated_at
        self.base_no_kwargs.save()

        self.assertNotEqual(previous_date, self.base_no_kwargs.updated_at)

    def test_to_dict_method(self):
        """ tests on to_dict method.
        """
        new_dict = self.base_no_kwargs.to_dict()
        self.assertIsInstance(new_dict, dict)
        # check of all the dates objects have been converted to string format
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertIsNotNone(new_dict["__class__"])
        self.assertIsInstance(new_dict["__class__"], str)

    def test_base_model_to_string(self):
        """ test if base model can be represented as a string
        """
        self.assertIsInstance(str(self.base_no_kwargs), str)

    def test_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            self.base_no_kwargs.to_dict("cool")

    def test_save_method_with_args(self):
        with self.assertRaises(TypeError):
            self.base_no_kwargs.save("cool")

    def tearDown(self):
        self.base_no_kwargs = None
        self.base_with_kwargs = None
        self.yesterday = None


if __name__ == "__main__":
    unittest.main()

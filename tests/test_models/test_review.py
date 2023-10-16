#!/usr/bin/python3
""" module to test FileStorage class.
"""

import unittest
from datetime import datetime, timedelta
import os

from models import storage
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """ class TestReview to test Review class.
    """
    def setUp(self):
        """ initialize class
        """
        self.review_no_kwargs = None
        self.review_with_kwargs = None
        self.yesterday = datetime.now() - timedelta(days=1)
        self.all_objs = storage.all()
        self.size = len(self.all_objs)  # number of items in storage

    def test_all_attributes_are_present(self):
        """ test all attributes are present
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        self.assertTrue(hasattr(self.review_no_kwargs, "id"))
        self.assertTrue(hasattr(self.review_no_kwargs, "place_id"))
        self.assertTrue(hasattr(self.review_no_kwargs, "user_id"))
        self.assertTrue(hasattr(self.review_no_kwargs, "text"))
        self.assertTrue(hasattr(self.review_no_kwargs, "created_at"))
        self.assertTrue(hasattr(self.review_no_kwargs, "updated_at"))

    def test_all_attributes_data_types(self):

        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()

        self.assertIsInstance(self.review_no_kwargs.id, str)
        self.assertIsInstance(self.review_no_kwargs.place_id, str)
        self.assertIsInstance(self.review_no_kwargs.user_id, str)
        self.assertIsInstance(self.review_no_kwargs.text, str)
        self.assertIsInstance(self.review_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.review_no_kwargs.updated_at, datetime)

    def test_add_new_attribute(self):
        self.review_no_kwargs = Review()
        self.review_no_kwargs.test = "cool"
        self.review_no_kwargs.save()

        self.assertTrue(hasattr(self.review_no_kwargs, "test"))

    def test_review_subclass_of_base_model(self):
        """ check if Review inherits from BaseModel
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        assert issubclass(type(self.review_no_kwargs), (BaseModel,))

    def test_save_review(self):
        """ test save method
        """
        new_size = self.size
        review = Review()
        review.save()

        self.all_objs = storage.all()
        self.size = len(self.all_objs)

        self.assertIsInstance(self.all_objs, dict)
        self.assertGreater(self.size, new_size)

    def test_update_at_is_modified_on_save(self):
        self.review_no_kwargs = Review()
        self.review_no_kwargs.updated_at = self.yesterday
        previous_date = self.review_no_kwargs.updated_at
        self.review_no_kwargs.save()

        self.assertNotEqual(previous_date, self.review_no_kwargs.updated_at)

    def test_create_review_no_kwargs(self):
        """ create Review with no **kwargs
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        self.review_no_kwargs.updated_at = self.yesterday
        to_dict = self.review_no_kwargs.to_dict()

        self.assertIsInstance(self.review_no_kwargs, Review)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_create_review_with_kwargs(self):
        """ create Review with **kwargs
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        self.review_with_kwargs = Review(**self.review_no_kwargs.to_dict())
        self.review_with_kwargs.updated_at = self.yesterday
        to_dict = self.review_with_kwargs.to_dict()

        self.assertIsInstance(self.review_with_kwargs, Review)
        self.assertIsInstance(to_dict, dict)
        self.assertIsNotNone(to_dict.get("__class__"))

    def test_id_is_string(self):
        """ check if id attribute contains a string.
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        self.assertIsInstance(self.review_no_kwargs.id, str)

    def test_dates_are_datetime_object(self):
        """ check if all dates in Review object are datetime objects
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        self.assertIsInstance(self.review_no_kwargs.created_at, datetime)
        self.assertIsInstance(self.review_no_kwargs.updated_at, datetime)

    def test_to_dict_method(self):
        """ tests on to_dict method.
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        new_dict = self.review_no_kwargs.to_dict()
        self.assertIsInstance(new_dict, dict)
        # check of all the dates objects have been converted to string format
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertIsNotNone(new_dict["__class__"])
        self.assertIsInstance(new_dict["__class__"], str)

    def test_review_to_string(self):
        """ test if Review can be represented as a string
        """
        self.review_no_kwargs = Review()
        self.review_no_kwargs.save()
        self.assertIsInstance(str(self.review_no_kwargs), str)

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

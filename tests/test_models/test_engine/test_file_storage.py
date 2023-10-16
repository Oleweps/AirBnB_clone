#!/usr/bin/python3
""" module to test FileStorage class
"""

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

import unittest
import os
import json


class TestFileStorage(unittest.TestCase):
    """ Class to test FileStorage class
    """
    def setUp(self):
        """ initialize tests
        """
        self.all_objs = storage.all()
        self.size = len(self.all_objs)

    def test_create_new_instance_no_args(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_create_new_instance_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage("cool")

    def test_invoke_none_existent_method(self):
        with self.assertRaises(AttributeError):
            FileStorage().run()

    def test_storage_is_instance_of_filestorage(self):
        self.assertIsInstance(storage, FileStorage)

    def test_private_attributes_not_accessible(self):
        self.assertFalse(hasattr(storage, "__file_path"))
        self.assertFalse(hasattr(storage, "__objects"))

    def test_all_method(self):
        """ test getting all objects
        """
        self.all_objs = storage.all()
        self.assertIsInstance(self.all_objs, dict)

    def test_new_method_valid_data(self):
        """ test adding a new Object
        """
        new_size = self.size
        base_model = BaseModel()
        storage.new(base_model)
        self.all_objs = storage.all()
        self.size = len(self.all_objs)
        self.assertGreater(self.size, new_size)

    def test_new_method_invalid_data(self):
        """ test adding invalid object
        """
        new_size = self.size
        storage.new("test")
        self.all_objs = storage.all()
        self.size = len(self.all_objs)
        self.assertEqual(self.size, new_size)

    def test_json_file_exists(self):
        """ check if json file is created
        """
        base_model = BaseModel()
        base_model.save()
        self.assertTrue(os.path.exists("storage.json"))

    def test_file_contains_json_data(self):
        """ check if file contains json
        """
        base_model = BaseModel()
        base_model.save()

        data = ""
        with open("storage.json", "r") as file:
            data = json.loads(file.read())

        self.assertIsInstance(data, dict)

    def test_reload_method_return_value(self):
        self.assertIsNone(storage.reload())

    def test_new_method_return_value(self):
        self.assertIsNone(storage.new("test"))

    def test_all_method_return_value(self):
        self.assertIsInstance(storage.all(), dict)

    def test_id_in_dict(self):
        base_model = BaseModel()
        base_model.save()

        new_id = "{}.{}".format("BaseModel", base_model.id)

        with open("storage.json", "r") as file:
            data = file.read()
            self.assertIn(new_id, data)

    def test_save_method(self):
        """ test save method
        """
        new_size = self.size
        base_model = BaseModel()
        base_model.save()
        self.all_objs = storage.all()
        self.size = len(self.all_objs)
        self.assertGreater(self.size, new_size)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            storage.reload(None)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            storage.reload(None)

    def tearDown(self):
        """ teardown function
        """
        self.all_objs = None
        self.size = 0
        if os.path.exists("storage.json"):
            os.remove("storage.json")


if __name__ == "__main__":
    unittest.main()

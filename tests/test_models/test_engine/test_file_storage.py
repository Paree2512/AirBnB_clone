#!/usr/bin/python3

import os
import json
import models
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class TestFileStorage(unittest.TestCase):
    """
    Unit tests for the FileStorage class.
    Attributes:
        file_storage (FileStorage): Instance of FileStorage for testing.
        test_filename (str): Name of the test JSON file used during testing
    Methods:
        setUp(); tearDown();
        test_all(); test_all_with_arg();
        test_new(); test_save();
        test_reload(); test_reload_with_arg();
    """

    def setUp(self):
        """Initializes the FileStorage instance and test file for testing"""
        self.file_storage = FileStorage()
        self.test_filename = "test_file.json"

    def tearDown(self):
        """Cleans up any test files created during testing"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_all(self):
        """Test the 'all' method to return the dictionary of stored objects"""
        self.assertIsInstance(self.file_storage.all(), dict)

    def test_all_with_arg(self):
        """Test 'all' method with an argument (should raise TypeError)"""
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        """Test the 'new' method to add an object to the stored objects"""
        base_model = BaseModel()
        self.file_storage.new(base_model)
        key = "{}.{}".format(base_model.__class__.__name__, base_model.id)
        self.assertIn(key, self.file_storage.all())

    def test_save(self):
        """Test the 'save' method to serialize stored objects to a JSON file"""
        bm = BaseModel()
        models.storage.new(bm)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)

    def test_reload(self):
        """Test the 'reload' method to load objects from a JSON file"""
        bm = BaseModel()
        models.storage.new(bm)
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)

    def test_reload_with_arg(self):
        """Test 'reload' method with an argument (should raise TypeError)"""
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_class_list_unregistered_class(self):
        """Test creating an object for an unregistered class"""
        class_name = "UnregisteredClass"
        data = {"_class_": class_name, "id": "test_id"}
        with open(self.test_filename, "w") as f:
            json.dump({"{}.test_id".format(class_name): data}, f)
        self.file_storage.FileStorage_objects = {}
        self.file_storage.reload()
        self.assertNotIn("{}.test_id".format(class_name),
                         self.file_storage.all())


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass
        FileStorage.FileStorage_objects = {}

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass
        FileStorage.FileStorage_objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        us = User()
        st = State()
        pl = Place()
        cy = City()
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        self.assertIn("User." + us.id, models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        bm = BaseModel()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + rv.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + us.id, objs)
        self.assertIn("State." + st.id, objs)
        self.assertIn("Place." + pl.id, objs)
        self.assertIn("City." + cy.id, objs)
        self.assertIn("Amenity." + am.id, objs)
        self.assertIn("Review." + rv.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == '__main__':
    unittest.main()

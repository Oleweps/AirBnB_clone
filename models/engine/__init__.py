#!/usr/bin/python3
""" a unique FileStorage instance for your application """
from models.engine.file_storage import FileStorage

""" A variable storage which is an instance of FileStorage """
storage = FileStorage()
storage.reload()

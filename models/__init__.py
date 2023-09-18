#!/usr/bin/python3
"""Instantiates a storage objects
Creating an instance of DBStorage and store it in the variable storage
Creating an instance of FileStorage and store it in the variable storage
if the value of the environment variable is db,
then we use SQL database, else JSON file as storage.
"""
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()

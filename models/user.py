#!/usr/bin/python3
""" module for implementation of User class.
"""
from models.base_model import BaseModel


class User(BaseModel):
    """ class User that defines a user."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

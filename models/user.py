#!/usr/bin/python3
""" a module for implementation of User class.
"""
from models.base_model import BaseModel


class User(BaseModel):
    """ class User that defines a user object."""

    def __init__(self, *args, **kwargs):
        """Initialize User object."""
        super().__init__(*args, **kwargs)

        email = ""
        password = ""
        first_name = ""
        last_name = ""

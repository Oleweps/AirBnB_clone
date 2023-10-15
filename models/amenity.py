#!/usr/bin/python3
""" a module for implementation of Amenity class
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """ class Amenity that defines the amenities. """
    def __init__(self, *args, **kwargs):
        """Initialize User object."""
        super().__init__(*args, **kwargs)
        self.name = ""

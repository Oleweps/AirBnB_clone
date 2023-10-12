#!/usr/bin/python3
""" a module for implementation of City class.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """ class City that defines a city. """

    def __init__(self, *args, **kwargs):
        """Initialize City object."""
        super().__init__(*args, **kwargs)

        state_id: str = ""
        name: str = ""

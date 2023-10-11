#!/usr/bin/python3
""" module for implementation of City class.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """ class City that defines a city. """

    state_id: str = ""
    name: str = ""

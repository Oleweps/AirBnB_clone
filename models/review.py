#!/usr/bin/python3
""" module for implementation of Review class.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """ class Review that defines a review. """

    place_id: str = ""
    user_id: str = ""
    text: str = ""

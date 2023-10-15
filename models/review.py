#!/usr/bin/python3
""" a module for implementation of Review class.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """ class Review that defines a review instance. """

    def __init__(self, *args, **kwargs):
        """Initialize Review object."""
        super().__init__(*args, **kwargs)

        self.place_id: str = ""
        self.user_id: str = ""
        self.text: str = ""

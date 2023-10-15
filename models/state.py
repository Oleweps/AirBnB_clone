#!/usr/bin/python3
""" a module for implementation of State class.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """ class State that defines a state object """

    def __init__(self, *args, **kwargs):
        """Initialize   State object."""
        super().__init__(*args, **kwargs)

        self.name: str = ""

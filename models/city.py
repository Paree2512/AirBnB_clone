#!/usr/bin/python3

"""City Module"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    City class that inherits from BaseModel.
    Attributes:
        name string - empty string (becomes the name of the city)
            state_id - empty string (will be the State.id from state class)
    """
    state_id = ""
    name = ""

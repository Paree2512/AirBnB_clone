#!/usr/bin/python3

"""Review Module"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class that inherits from BaseModel.
    Attributes:
        text (str): review details of a place
        place_id (str): id of the place a user is looking into
        user_id (str): User id
    """
    place_id = ""  # This will be the Place.id
    user_id = ""  # This will be the User.id
    text = ""

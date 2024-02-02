'''Contains Player class'''

from typing import Dict

from config.string_constants import Roles
from models.users.user import User


class Player(User):
    '''
    Class representing a player user.

    Inherits from:
        User: Abstract Class for representing users.

    Methods:
        get_instance(): Create a new instance of Player class.
    '''

    @classmethod
    def get_instance(cls, user_data: Dict[str, str], role: str=None) -> 'Player':
        'Factory method to create a new instance of Player model.'

        return super().get_instance(user_data, role=Roles.PLAYER)

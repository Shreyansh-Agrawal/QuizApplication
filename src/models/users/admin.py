'''Contains Admin Class'''

from typing import Dict

from config.string_constants import Roles
from models.users.user import User


class Admin(User):
    '''
    Class representing an admin user.

    Inherits from:
        User: Abstract Class for representing users.

    Methods:
        get_instance(): Create a new instance of Admin class.
    '''

    @classmethod
    def get_instance(cls, user_data: Dict[str, str], role: str=None) -> 'Admin':
        'Factory method to create a new instance of Admin model.'

        return super().get_instance(user_data, role=Roles.ADMIN)

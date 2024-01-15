'''Contains SuperAdmin abstract class'''

from typing import Dict

from models.users.user import User


class SuperAdmin(User):
    '''
    Class representing a super admin user.

    Inherits from:
        User: Abstract Base Class for representing users.

    Methods:
        get_instance(): Create a new instance of SuperAdmin class.
    '''

    @classmethod
    def get_instance(cls, user_data: Dict[str, str], role: str=None) -> 'SuperAdmin':
        'Factory method to create a new instance of SuperAdmin class.'

        return super().get_instance(user_data, role='super admin')

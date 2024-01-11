'''Contains SuperAdmin abstract class'''

from typing import Dict

from models.database.database_saver import DatabaseSaver
from models.users.user import User
from models.users.user_manager import UserManager


class SuperAdmin(User, DatabaseSaver):
    '''
    Class representing a super admin user.

    Inherits from:
        User: Abstract Base Class for representing users.
        DatabaseSaver: Interface for saving to the database.

    Methods:
        save_to_database(): Saves the super admin to the database.
    '''

    def __init__(self, super_admin_data: Dict) -> None:
        '''
        Initializes a SuperAdmin instance.

        Args:
            super_admin_data (Dict): A dictionary containing super admin details.
        '''
        super().__init__(user_data=super_admin_data, role='super admin')

    def save_to_database(self) -> None:
        '''Save the super admin to the database.'''

        super_admin_manager = UserManager(self)
        super_admin_manager.save_to_database()

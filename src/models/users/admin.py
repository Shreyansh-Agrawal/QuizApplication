'''Contains Admin Class'''

from typing import Dict

from models.database.database_saver import DatabaseSaver
from models.users.user import User
from models.users.user_manager import UserManager


class Admin(User, DatabaseSaver):
    '''
    Class representing an admin user.

    Inherits from:
        User: Abstract Base Class for representing users.
        DatabaseSaver: Interface for saving to the database.

    Methods:
        save_to_database(): Saves the admin to the database.
    '''

    def __init__(self, admin_data: Dict) -> None:
        '''
        Initializes an Admin instance.

        Args:
            admin_data (Dict): A dictionary containing admin details.
        '''
        super().__init__(user_data=admin_data, role='admin')

    def save_to_database(self) -> None:
        '''Save the admin to the database.'''

        admin_manager = UserManager(self)
        admin_manager.save_to_database()

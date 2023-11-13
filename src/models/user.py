'''Contains classes for Super Admin, Admin, Player'''

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict

from config.queries import Queries
from database.database_access import DatabaseAccess as DAO
from utils import validations


class User(ABC):
    '''Abstract Base Class for representing users.'''

    def __init__(self, user_data: Dict, role: str) -> None:
        self.name = user_data.get('name')
        self.email = user_data.get('email')
        self.username = user_data.get('username')
        self.password = user_data.get('password')
        self.user_id = validations.validate_id(entity=role)
        self.role = role
        self.is_password_changed = 0 if role == 'admin' else 1
        self.registration_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')


class DatabaseSaver(ABC):
    '''Abstract interface for saving to the database'''

    @abstractmethod
    def save_to_database(self) -> None:
        '''Abstract method to save to the database'''
        pass


class UserManager:
    '''
    Manager class responsible for saving users to the database.

    Attributes:
        user (User): The user object to be managed.
    '''

    def __init__(self, user: User) -> None:
        self.user = user

    def save_to_database(self) -> None:
        '''
        Saves the user and their credentials to the database.
        '''
        user_data = (
            self.user.user_id,
            self.user.name,
            self.user.email,
            self.user.role,
            self.user.registration_date
        )

        credentials = (
            self.user.user_id,
            self.user.username,
            self.user.password,
            self.user.is_password_changed
        )

        DAO.write_to_database(Queries.INSERT_USER_DATA, user_data)
        DAO.write_to_database(Queries.INSERT_CREDENTIALS, credentials)


class SuperAdmin(User, DatabaseSaver):
    '''Class representing a super admin user.'''

    def __init__(self, super_admin_data: Dict) -> None:
        super().__init__(user_data=super_admin_data, role='super admin')

    def save_to_database(self) -> None:
        '''Save the super admin to the database.'''

        super_admin_manager = UserManager(self)
        super_admin_manager.save_to_database()


class Admin(User, DatabaseSaver):
    '''Class representing an admin user.'''

    def __init__(self, admin_data: Dict) -> None:
        super().__init__(user_data=admin_data, role='admin')

    def save_to_database(self) -> None:
        '''Save the admin to the database.'''

        admin_manager = UserManager(self)
        admin_manager.save_to_database()


class Player(User, DatabaseSaver):
    '''Class representing a player user.'''

    def __init__(self, player_data: Dict) -> None:
        super().__init__(user_data=player_data, role='player')

    def save_to_database(self) -> None:
        '''Save the player to the database.'''

        player_manager = UserManager(self)
        player_manager.save_to_database()

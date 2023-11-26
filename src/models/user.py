'''Contains classes for Super Admin, Admin, Player'''

from abc import ABC
from datetime import datetime, timezone
from typing import Dict

from models.database_saver import DatabaseSaver
from models.user_manager import UserManager
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

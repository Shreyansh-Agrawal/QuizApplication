'''Contains classes for Super Admin, Admin, User'''

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict

from config.queries import Queries
from database.database_access import DatabaseAccess as DAO
from utils import validations


class Person(ABC):
    '''Abstract Base Class'''

    def __init__(self, name: str, email: str, username: str, password: str) -> None:
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.registration_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    @abstractmethod
    def save_user_to_database(self) -> None:
        ''''abstract method to create a new user'''


class SuperAdmin(Person):
    '''Super Admin class'''

    def __init__(self, super_admin_data: Dict) -> None:
        super().__init__(
            super_admin_data.get('name'),
            super_admin_data.get('email'),
            super_admin_data.get('username'),
            super_admin_data.get('password')
        )

        self.user_id = validations.validate_id(entity='super_admin')
        self.role = 'super admin'
        self.is_password_changed = 1

    def save_user_to_database(self) -> None:
        '''method to add user to database'''

        super_admin_data = (
            self.user_id,
            self.name,
            self.email,
            self.role,
            self.registration_date
        )

        credentials = (
            self.user_id,
            self.username,
            self.password,
            self.is_password_changed
        )

        DAO.write_to_database(Queries.INSERT_USER_DATA, super_admin_data)
        DAO.write_to_database(Queries.INSERT_CREDENTIALS, credentials)


class Admin(Person):
    '''Admin class'''

    def __init__(self, admin_data: Dict) -> None:
        super().__init__(
            admin_data.get('name'),
            admin_data.get('email'),
            admin_data.get('username'),
            admin_data.get('password')
            )

        self.user_id = validations.validate_id(entity='admin')
        self.role = 'admin'
        self.is_password_changed = 0

    def save_user_to_database(self) -> None:
        '''method to add user to database'''

        admin_data = (
            self.user_id,
            self.name,
            self.email,
            self.role,
            self.registration_date
        )

        credentials = (
            self.user_id,
            self.username,
            self.password,
            self.is_password_changed
        )

        DAO.write_to_database(Queries.INSERT_USER_DATA, admin_data)
        DAO.write_to_database(Queries.INSERT_CREDENTIALS, credentials)


class User(Person):
    '''User class'''

    def __init__(self, user_data: Dict) -> None:
        super().__init__(
            user_data.get('name'),
            user_data.get('email'),
            user_data.get('username'),
            user_data.get('password')
        )

        self.user_id = validations.validate_id(entity='user')
        self.role = 'user'
        self.is_password_changed = 1

    def save_user_to_database(self) -> None:
        '''method to add user to database'''

        user_data = (
            self.user_id,
            self.name,
            self.email,
            self.role,
            self.registration_date
        )

        credentials = (
            self.user_id,
            self.username,
            self.password,
            self.is_password_changed
        )

        DAO.write_to_database(Queries.INSERT_USER_DATA, user_data)
        DAO.write_to_database(Queries.INSERT_CREDENTIALS, credentials)

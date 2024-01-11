'''Contains User abstract class'''

from abc import ABC
from datetime import datetime, timezone
from typing import Dict

from utils import validations


class User(ABC):
    '''
    Abstract Base Class for representing users.

    Attributes:
        name (str): The user's name.
        email (str): The user's email address.
        username (str): The user's username.
        password (str): The user's password.
        user_id (str): The unique identifier for the user.
        role (str): The user's role (super admin, admin, player).
        is_password_changed (int): Flag indicating if the user has changed their password.
        registration_date (str): The date and time of user registration in UTC format.
    '''

    def __init__(self, user_data: Dict, role: str) -> None:
        '''
        Initializes a User instance.

        Args:
            user_data (Dict): A dictionary containing user details.
            role (str): The role of the user.

        Raises:
            KeyError: If required user data is missing.
        '''
        self.name = user_data.get('name')
        self.email = user_data.get('email')
        self.username = user_data.get('username')
        self.password = user_data.get('password')
        self.user_id = validations.validate_id(entity=role)
        self.role = role
        self.is_password_changed = 0 if role == 'admin' else 1
        self.registration_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

'''Contains User abstract class'''

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict

from utils.id_generator import generate_id


@dataclass
class User(ABC):
    '''
    Abstract Class for representing users.

    Attributes:
        name (str): The user's name.
        email (str): The user's email address.
        username (str): The user's username.
        password (str): The user's password.
        role (str): The user's role (super_admin, admin, player).
        user_id (str): The unique identifier for the user.
        is_password_changed (int): Flag indicating if the user has changed their password.
        registration_date (str): The date and time of user registration in UTC format.
    '''
    user_id: str = field(init=False)
    name: str
    email: str
    role: str
    registration_date: str = field(init=False)
    username: str
    password: str
    is_password_changed: int = field(init=False)

    def __post_init__(self) -> None:
        self.is_password_changed = 0 if self.role == 'admin' else 1
        self.user_id = generate_id(entity=self.role)
        self.registration_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    @classmethod
    def get_instance(cls, user_data: Dict[str, str], role) -> 'User':
        '''
        Factory method to create a new instance of User model.

        Args:
            user_data (Dict): A dictionary containing user details.

        Returns:
            User: An instance of the User class.
        '''
        return cls(
            name=user_data.get('name'),
            email=user_data.get('email'),
            username=user_data.get('username'),
            password=user_data.get('password'),
            role=role
        )

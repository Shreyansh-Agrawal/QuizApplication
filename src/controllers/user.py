'''Controllers for Operations related to Users: SuperAdmin, Admin, Player'''

import logging
import random
import string
from typing import Dict, List, Tuple

import mysql.connector

from config.message_prompts import ErrorMessage, Headers, LogMessage, Roles
from config.queries import Queries
from models.database.user_db import UserDB
from models.users.admin import Admin
from utils.custom_error import DuplicateEntryError
from utils.password_hasher import hash_password

logger = logging.getLogger(__name__)


class UserController:
    '''UserController class for user management'''

    def __init__(self, database) -> None:
        self.db = database
        self.user_db = UserDB(self.db)

    def get_user_id(self, username: str) -> str:
        '''Return user's id'''

        data = self.db.read(Queries.GET_USER_ID_BY_USERNAME, (username, ))
        return data

    def get_all_users_by_role(self, role: str) -> List[Tuple]:
        '''Return all users with their details'''

        data = self.db.read(Queries.GET_USER_BY_ROLE, (role, ))
        return data

    def get_user_profile_data(self, user_id: str) -> str:
        '''Return user's profile data'''

        data = self.db.read(Queries.GET_USER_BY_USER_ID, (user_id, ))
        return data

    def create_admin(self, admin_data: Dict) -> None:
        '''Create a new Admin Account'''

        characters = string.ascii_letters + string.digits + '@#$&'
        password = ''.join(random.choice(characters) for _ in range(6))
        admin_data['password'] = password
        admin = Admin.get_instance(admin_data)
        try:
            self.user_db.save(admin)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.USER_EXISTS_ERROR) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.ADMIN)

    def update_user_data(self, user_id: str, user_data: Dict):
        '''Update user profile'''

        users_query = 'UPDATE users SET '
        credentials_query = 'UPDATE credentials SET '
        users_update_values = []
        credentials_update_values = []

        if 'name' in user_data:
            users_query += 'name = %s, '
            users_update_values.append(user_data['name'])

        if 'email' in user_data:
            users_query += 'email = %s, '
            users_update_values.append(user_data['email'])

        if 'username' in user_data:
            credentials_query += 'username = %s, '
            credentials_update_values.append(user_data['username'])

        if 'password' in user_data:
            credentials_query += 'password = %s, '
            credentials_update_values.append(hash_password(user_data['password']))

        # Remove the trailing comma and space
        users_query = users_query.rstrip(', ')
        credentials_query = credentials_query.rstrip(', ')

        users_query += ' WHERE user_id = %s'
        credentials_query += ' WHERE user_id = %s'
        users_update_values.append(user_id)
        credentials_update_values.append(user_id)
        try:
            if len(users_update_values) > 1:
                self.db.write(users_query, tuple(users_update_values))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity='Email')) from e
        try:
            if len(credentials_update_values) > 1:
                self.db.write(credentials_query, tuple(credentials_update_values))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity='Username')) from e

    def delete_admin_by_id(self, user_id: str) -> None:
        '''Delete a User'''

        row_affected = self.db.write(Queries.DELETE_USER_BY_ID_ROLE, (user_id, Roles.ADMIN))
        logger.debug(LogMessage.DELETE_SUCCESS, Roles.ADMIN)
        return row_affected

    def delete_player_by_id(self, user_id: str) -> None:
        '''Delete a User'''

        row_affected = self.db.write(Queries.DELETE_USER_BY_ID_ROLE, (user_id, Roles.PLAYER))
        logger.debug(LogMessage.DELETE_SUCCESS, Roles.PLAYER)
        return row_affected

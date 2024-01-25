'''Business for Operations related to Users: SuperAdmin, Admin, Player'''

import logging
from typing import Dict, List

import mysql.connector

from config.message_prompts import ErrorMessage, Headers, LogMessage, Roles, StatusCodes
from config.queries import Queries
from models.database.user_db import UserDB
from models.users.admin import Admin
from utils.custom_error import DataNotFoundError, DuplicateEntryError
from utils.password_hasher import hash_password
from utils.password_generator import generate_password

logger = logging.getLogger(__name__)


class UserBusiness:
    '''UserBusiness class for user management'''

    def __init__(self, database) -> None:
        self.db = database
        self.user_db = UserDB(self.db)

    def get_all_users_by_role(self, role: str) -> List[Dict]:
        '''Return all users with their details'''

        data = self.db.read(Queries.GET_USER_BY_ROLE, (role, ))
        if not data:
            raise DataNotFoundError(StatusCodes.NOT_FOUND, message=ErrorMessage.USER_NOT_FOUND)
        return data

    def get_user_profile_data(self, user_id: str) -> str:
        '''Return user's profile data'''

        data = self.db.read(Queries.GET_USER_BY_USER_ID, (user_id, ))
        if not data:
            raise DataNotFoundError(StatusCodes.NOT_FOUND, message=ErrorMessage.USER_NOT_FOUND)
        return data

    def create_admin(self, admin_data: Dict) -> None:
        '''Create a new Admin Account'''

        admin_data['password'] = generate_password()
        admin = Admin.get_instance(admin_data)
        try:
            self.user_db.save(admin)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(StatusCodes.CONFLICT, message=ErrorMessage.USER_EXISTS) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.ADMIN)

    def update_user_data(self, user_id: str, user_data: Dict) -> None:
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
            credentials_query += 'isPasswordChanged = 1, '
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
            raise DuplicateEntryError(StatusCodes.CONFLICT, message=ErrorMessage.EMAIL_TAKEN) from e
        try:
            if len(credentials_update_values) > 1:
                self.db.write(credentials_query, tuple(credentials_update_values))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(StatusCodes.CONFLICT, message=ErrorMessage.USERNAME_TAKEN) from e

    def delete_user_by_id(self, user_id: str, role: str) -> None:
        '''Delete a user by id and role'''

        row_affected = self.db.write(Queries.DELETE_USER_BY_ID_ROLE, (user_id, role))
        if not row_affected:
            raise DataNotFoundError(StatusCodes.NOT_FOUND, message=ErrorMessage.USER_NOT_FOUND)

        logger.debug(LogMessage.DELETE_SUCCESS, Roles.PLAYER)
        return row_affected

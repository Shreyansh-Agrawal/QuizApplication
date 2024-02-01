'''Business logic for Operations related to Users: SuperAdmin, Admin, Player'''

import logging
from typing import Dict, List

import mysql.connector

from config.message_prompts import ErrorMessage, Headers, LogMessage, Roles, StatusCodes
from config.queries import Queries
from models.users.admin import Admin
from helpers.user_helper import UserHelper
from utils.custom_error import DataNotFoundError, DuplicateEntryError, InvalidCredentialsError
from utils.password_hasher import hash_password
from utils.password_generator import generate_password

logger = logging.getLogger(__name__)


class UserBusiness:
    '''UserBusiness class for user management'''

    def __init__(self, database) -> None:
        self.db = database
        self.user_helper = UserHelper(self.db)

    def get_all_users_by_role(self, role: str) -> List[Dict]:
        '''Return all users with their details'''

        data = self.db.read(Queries.GET_USER_BY_ROLE, (role, ))
        if not data:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.USER_NOT_FOUND)
        return data

    def get_user_profile_data(self, user_id: str) -> str:
        '''Return user's profile data'''

        data = self.db.read(Queries.GET_USER_BY_USER_ID, (user_id, ))
        if not data:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.USER_NOT_FOUND)
        return data

    def create_admin(self, admin_data: Dict) -> None:
        '''Create a new Admin Account'''

        admin_data['password'] = generate_password()
        admin = Admin.get_instance(admin_data)
        try:
            self.user_helper.save_user(admin)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.USER_EXISTS) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.ADMIN)

    def update_user_data(self, user_id: str, user_data: Dict) -> None:
        '''Update user profile'''

        name, email, username = user_data['name'], user_data['email'], user_data['username']
        try:
            self.db.write(Queries.UPDATE_USER_PROFILE, (name, email, user_id))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.EMAIL_TAKEN) from e
        try:
            self.db.write(Queries.UPDATE_USERNAME, (username, user_id))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.USERNAME_TAKEN) from e

    def update_user_password(self, user_id: str, password_data: Dict) -> None:
        '''Update user password'''

        current_password, new_password = password_data['current_password'], password_data['new_password']
        hashed_current_password = hash_password(current_password)
        user_password_data = self.db.read(Queries.GET_PASSWORD_BY_USER_ID, (user_id, ))
        user_password = user_password_data[0]['password']

        if user_password not in (current_password, hashed_current_password):
            raise InvalidCredentialsError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIALS)

        new_password = hash_password(new_password)
        self.db.write(Queries.UPDATE_USER_PASSWORD, (new_password, user_id))

    def delete_user_by_id(self, user_id: str, role: str) -> None:
        '''Delete a user by id and role'''

        row_affected = self.db.write(Queries.DELETE_USER_BY_ID_ROLE, (user_id, role))
        if not row_affected:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.USER_NOT_FOUND)

        logger.debug(LogMessage.DELETE_SUCCESS, Roles.PLAYER)
        return row_affected

'''Business Logic for Operations related to Authentication'''

import logging
from typing import Dict

import mysql.connector
from flask_jwt_extended import create_access_token, create_refresh_token

from config.message_prompts import ErrorMessage, LogMessage, StatusCodes
from config.queries import Queries
from database.database_access import DatabaseAccess
from models.database.user_db import UserDB
from models.users.player import Player
from utils.blocklist import BLOCKLIST
from utils.custom_error import DuplicateEntryError, InvalidCredentialsError
from utils.password_hasher import hash_password
from utils.rbac import ROLE_MAPPING

logger = logging.getLogger(__name__)


class AuthBusiness:
    '''AuthBusiness class containing login and signup methods'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.user_db = UserDB(self.db)

    def login(self, login_data: Dict) -> Dict:
        '''Method for user login'''

        logger.debug(LogMessage.LOGIN_INITIATED)

        username, password = login_data.values()
        hashed_password = hash_password(password)
        user_data = self.db.read(Queries.GET_CREDENTIALS_BY_USERNAME, (username, ))

        if not user_data:
            raise InvalidCredentialsError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIALS)
        user_id, user_password, role, is_password_changed = user_data[0].values()

        if user_password not in (password, hashed_password):
            raise InvalidCredentialsError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIALS)

        mapped_role = ROLE_MAPPING.get(role)
        access_token = create_access_token(
            identity=user_id,
            fresh=True,
            additional_claims={'cap': mapped_role}
        )
        refresh_token = create_refresh_token(
            identity=user_id,
            additional_claims={'cap': mapped_role}
        )
        password_type = 'permanent' if is_password_changed else 'default'
        token_data = {"access_token": access_token, "refresh_token": refresh_token, "password_type": password_type}
        return token_data

    def register(self, player_data: Dict) -> None:
        '''Method for signup, only for player'''

        logger.debug(LogMessage.SIGNUP_INITIATED)

        player_data['password'] = hash_password(player_data['password'])
        player = Player.get_instance(player_data)
        try:
            self.user_db.save(player)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(StatusCodes.CONFLICT, message=ErrorMessage.USER_EXISTS) from e

        logger.debug(LogMessage.SIGNUP_SUCCESS)

    def logout(self, token_id: str) -> None:
        '''Method to logout an authenticated user'''

        BLOCKLIST.add(token_id)

    def refresh(self, user_id: str, mapped_role: str) -> Dict:
        '''Method to get a non fresh access token'''

        new_access_token = create_access_token(
            identity=user_id,
            fresh=False,
            additional_claims={'cap': mapped_role}
        )
        token_data = {"access_token": new_access_token}
        return token_data

'''Business Logic for Operations related to Authentication'''

import logging
from typing import Dict, Tuple

import mysql.connector

from config.message_prompts import ErrorMessage, LogMessage, StatusCodes
from config.queries import Queries
from database.database_access import DatabaseAccess
from models.database.user_db import UserDB
from models.users.player import Player
from utils.custom_error import DuplicateEntryError, InvalidCredentialsError
from utils.password_hasher import hash_password

logger = logging.getLogger(__name__)


class AuthBusiness:
    '''AuthBusiness class containing login and signup methods'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.user_db = UserDB(self.db)

    def login(self, username: str, password: str) -> Tuple:
        '''Method for user login'''

        logger.debug(LogMessage.LOGIN_INITIATED)
        hashed_password = hash_password(password)
        user_data = self.db.read(Queries.GET_CREDENTIALS_BY_USERNAME, (username, ))

        if not user_data:
            raise InvalidCredentialsError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIALS)
        user_id, user_password, role, is_password_changed = user_data[0].values()

        if user_password not in (password, hashed_password):
            raise InvalidCredentialsError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIALS)

        logger.debug(LogMessage.LOGIN_SUCCESS)
        return user_id, role, is_password_changed

    def register(self, player_data: Dict) -> str:
        '''Method for signup, only for player'''

        logger.debug(LogMessage.SIGNUP_INITIATED)

        player_data['password'] = hash_password(player_data['password'])
        player = Player.get_instance(player_data)
        try:
            self.user_db.save(player)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(StatusCodes.CONFLICT, message=ErrorMessage.USER_EXISTS) from e

        logger.debug(LogMessage.SIGNUP_SUCCESS)

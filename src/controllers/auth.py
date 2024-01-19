'''Controllers for Operations related to Authentication'''

import logging
from typing import Dict, Tuple

import mysql.connector

from config.message_prompts import DisplayMessage, ErrorMessage, LogMessage
from config.queries import Queries
from database.database_access import DatabaseAccess
from models.users.player import Player
from models.database.user_db import UserDB
from utils.custom_error import LoginError
from utils.password_hasher import hash_password

logger = logging.getLogger(__name__)


class AuthController:
    '''AuthController class containing login and signup methods'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.user_db = UserDB(self.db)

    def login(self, username: str, password: str) -> Tuple:
        '''Method for user login'''

        logger.debug(LogMessage.LOGIN_INITIATED)
        hashed_password = hash_password(password)
        user_data = self.db.read(Queries.GET_CREDENTIALS_BY_USERNAME, (username, ))

        if not user_data:
            return ()
        user_password, role, is_password_changed = user_data[0].values()
        if user_password != password and user_password != hashed_password:
            return ()

        logger.debug(LogMessage.LOGIN_SUCCESS)
        return (username, role, is_password_changed)

    def signup(self, player_data: Dict) -> str:
        '''Method for signup, only for player'''

        logger.debug(LogMessage.SIGNUP_INITIATED)
        player_data['password'] = hash_password(player_data['password'])
        player = Player.get_instance(player_data)

        try:
            self.user_db.save(player)
        except mysql.connector.IntegrityError as e:
            raise LoginError(ErrorMessage.USER_EXISTS_ERROR) from e

        logger.debug(LogMessage.SIGNUP_SUCCESS)
        return player_data['username']

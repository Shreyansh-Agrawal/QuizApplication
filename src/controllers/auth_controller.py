'''Controllers for Operations related to Authentication'''

import logging
import sqlite3
from typing import Dict, Tuple

from config.message_prompts import DisplayMessage, LogMessage, ErrorMessage
from config.queries import Queries
from database.database_access import db
from models.user import Player
from utils.custom_error import LoginError
from utils.password_hasher import hash_password

logger = logging.getLogger(__name__)


class AuthController:
    '''AuthController class containing login and signup methods'''

    def login(self, username: str, password: str) -> Tuple:
        '''Method for user login'''

        logger.debug(LogMessage.LOGIN_INITIATED)
        hashed_password = hash_password(password)
        user_data = db.read_from_database(Queries.GET_CREDENTIALS_BY_USERNAME, (username, ))

        if not user_data:
            print(DisplayMessage.AUTH_INVALIDATE_MSG)
            return ()
        user_password, role, is_password_changed = user_data[0]
        if user_password != password and user_password != hashed_password:
            print(DisplayMessage.AUTH_INVALIDATE_MSG)
            return ()

        logger.debug(LogMessage.LOGIN_SUCCESS)
        print(DisplayMessage.LOGIN_SUCCESS_MSG)
        return (username, role, is_password_changed)

    def signup(self, player_data: Dict) -> str:
        '''Method for signup, only for player'''

        logger.debug(LogMessage.SIGNUP_INITIATED)
        player_data['password'] = hash_password(player_data['password'])
        player = Player(player_data)

        try:
            player.save_to_database()
        except sqlite3.IntegrityError as e:
            raise LoginError(ErrorMessage.USER_EXISTS_ERROR) from e

        logger.debug(LogMessage.SIGNUP_SUCCESS)
        print(DisplayMessage.SIGNUP_SUCCESS_MSG)
        return player_data['username']

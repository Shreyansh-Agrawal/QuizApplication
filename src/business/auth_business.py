'''Business Logic for Operations related to Authentication'''

import logging
from typing import Dict, Tuple

import pymysql

from config.queries import Queries
from config.string_constants import ErrorMessage, LogMessage, StatusCodes, PasswordTypes
from database.database_access import DatabaseAccess
from helpers.token_helper import TokenHelper
from helpers.user_helper import UserHelper
from models.users.player import Player
from utils.custom_error import DuplicateEntryError, InvalidCredentialsError
from utils.password_hasher import hash_password
from utils.rbac import ROLE_MAPPING

logger = logging.getLogger(__name__)


class AuthBusiness:
    '''AuthBusiness class containing login and signup methods'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.user_helper = UserHelper(self.db)
        self.token_helper = TokenHelper(self.db)

    def login(self, login_data: Dict) -> Dict:
        '''Method for user login'''

        logger.info(LogMessage.LOGIN_INITIATED)

        username, password = login_data['username'], login_data['password']
        hashed_password = hash_password(password)
        user_data = self.db.read(Queries.GET_CREDENTIALS_BY_USERNAME, (username, ))

        user_id, role, is_password_changed = self.__verify_credentials(user_data, password, hashed_password)
        mapped_role = ROLE_MAPPING.get(role)
        password_type = PasswordTypes.PERMANENT if is_password_changed else PasswordTypes.DEFAULT

        token_data = self.token_helper.generate_token_data(
            identity=user_id,
            mapped_role=mapped_role,
            is_fresh=True
        )
        token_data.update({"password_type": password_type})

        logger.info(LogMessage.TOKEN_CREATED)
        return token_data

    def __verify_credentials(self, user_data, password, hashed_password) -> Tuple:
        '''Match the password'''

        if not user_data:
            raise InvalidCredentialsError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIALS)
        user_id, user_password, role, is_password_changed = user_data[0].values()

        if user_password not in (password, hashed_password):
            raise InvalidCredentialsError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_CREDENTIALS)

        return user_id, role, is_password_changed

    def register(self, player_data: Dict) -> None:
        '''Method for signup, only for player'''

        logger.info(LogMessage.SIGNUP_INITIATED)

        player_data['password'] = hash_password(player_data['password'])
        player = Player.get_instance(player_data)
        try:
            self.user_helper.save_user(player)
        except pymysql.IntegrityError as e:
            logger.exception(e)
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.USER_EXISTS) from e

        logger.info(LogMessage.SIGNUP_SUCCESS)

    def logout(self, user_id: str) -> None:
        '''Method to logout an authenticated user'''

        logger.info(LogMessage.LOGOUT_INITIATED)
        self.token_helper.revoke_token(user_id)
        logger.info(LogMessage.LOGOUT_SUCCESS)

    def refresh(self, user_id: str, mapped_role: str) -> Dict:
        '''Method to get a non fresh access token'''

        logger.info(LogMessage.REFRESH_INITIATED)

        token_data = self.token_helper.generate_token_data(
            identity=user_id,
            mapped_role=mapped_role,
            is_fresh=False
        )
        logger.info(LogMessage.TOKEN_CREATED)
        return token_data

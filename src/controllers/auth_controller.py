'''Controllers for Operations related to Authentication'''

import logging
from typing import Dict

from business.auth_business import AuthBusiness
from config.message_prompts import Message, StatusCodes
from database.database_access import DatabaseAccess
from utils.custom_response import SuccessMessage
from utils.error_handlers import handle_custom_errors

logger = logging.getLogger(__name__)


class AuthController:
    '''AuthController class containing login and signup methods'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.auth_business = AuthBusiness(self.db)

    @handle_custom_errors
    def login(self, login_data: Dict):
        '''Method for user login'''

        token_data = self.auth_business.login(login_data)
        return SuccessMessage(status=StatusCodes.OK, message=Message.LOGIN_SUCCESS, data=token_data)

    @handle_custom_errors
    def register(self, player_data: Dict):
        '''Method for signup, only for player'''

        self.auth_business.register(player_data)
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.SIGNUP_SUCCESS)

    @handle_custom_errors
    def logout(self, token_id: str):
        '''Method to logout an authenticated user'''

        self.auth_business.logout(token_id)
        return SuccessMessage(status=StatusCodes.OK, message=Message.LOGOUT_SUCCESS)

    @handle_custom_errors
    def refresh(self, user_id: str, mapped_role: str):
        '''Method to get a non fresh access token'''

        data = self.auth_business.refresh(user_id, mapped_role)
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=data)

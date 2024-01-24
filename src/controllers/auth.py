'''Controllers for Operations related to Authentication'''

import logging
from typing import Dict, Tuple

from flask_jwt_extended import create_access_token, create_refresh_token

from business.auth import AuthBusiness
from config.message_prompts import Message, StatusCodes
from database.database_access import DatabaseAccess
from utils.blocklist import BLOCKLIST
from utils.custom_response import SuccessMessage
from utils.error_handlers import handle_custom_errors
from utils.rbac import ROLE_MAPPING

logger = logging.getLogger(__name__)


class AuthController:
    '''AuthController class containing login and signup methods'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.auth_business = AuthBusiness(self.db)

    @handle_custom_errors
    def login(self, login_data: Dict) -> Tuple:
        '''Method for user login'''

        username, password = login_data.values()
        user_data = self.auth_business.login(username, password)

        user_id, role, *_ = user_data
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
        data = {"access_token": access_token, "refresh_token": refresh_token}
        return SuccessMessage(status=StatusCodes.OK, message=Message.LOGIN_SUCCESS, data=data).message_info

    @handle_custom_errors
    def register(self, player_data: Dict) -> str:
        '''Method for signup, only for player'''

        self.auth_business.register(player_data)
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.SIGNUP_SUCCESS).message_info

    def logout(self, token_id: str):
        '''Method to logout an authenticated user'''

        BLOCKLIST.add(token_id)
        return SuccessMessage(status=StatusCodes.OK, message=Message.LOGOUT_SUCCESS).message_info

    def refresh(self, user_id: str, role: str):
        '''Method to get a non fresh access token'''

        new_access_token = create_access_token(
            identity=user_id,
            fresh=False,
            additional_claims={'cap': role}
        )
        data = {"access_token": new_access_token}
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=data).message_info

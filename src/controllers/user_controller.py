'''Controllers for Operations related to Users: SuperAdmin, Admin, Player'''

import logging
from typing import Dict

from business.user_business import UserBusiness
from config.message_prompts import Message, Roles, StatusCodes
from utils.custom_response import SuccessMessage
from utils.error_handlers import handle_custom_errors

logger = logging.getLogger(__name__)


class UserController:
    '''UserController class for user management'''

    def __init__(self, database) -> None:
        self.db = database
        self.user_business = UserBusiness(self.db)

    @handle_custom_errors
    def get_all_admins(self):
        '''Return all admins with their details'''

        admin_data = self.user_business.get_all_users_by_role(role=Roles.ADMIN)
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=admin_data).message_info

    @handle_custom_errors
    def get_all_players(self):
        '''Return all players with their details'''

        player_data = self.user_business.get_all_users_by_role(role=Roles.PLAYER)
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=player_data).message_info

    @handle_custom_errors
    def get_user_profile_data(self, user_id: str):
        '''Return user's profile data'''

        user_data = self.user_business.get_user_profile_data(user_id)
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=user_data[0]).message_info

    @handle_custom_errors
    def create_admin(self, admin_data: Dict):
        '''Create a new Admin Account'''

        self.user_business.create_admin(admin_data)
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.ADMIN_CREATED).message_info

    @handle_custom_errors
    def update_user_data(self, user_id: str, user_data: Dict):
        '''Update user profile'''

        self.user_business.update_user_data(user_id, user_data)
        return SuccessMessage(status=StatusCodes.OK, message=Message.PROFILE_UPDATED).message_info

    @handle_custom_errors
    def update_user_password(self, user_id: str, password_data: Dict):
        '''Update user password'''

        self.user_business.update_user_password(user_id, password_data)
        return SuccessMessage(status=StatusCodes.OK, message=Message.PASSWORD_UPDATED).message_info

    @handle_custom_errors
    def delete_admin_by_id(self, admin_id: str):
        '''Delete a Admin'''

        self.user_business.delete_user_by_id(admin_id, role=Roles.ADMIN)
        return SuccessMessage(status=StatusCodes.OK, message=Message.ADMIN_DELETED).message_info

    @handle_custom_errors
    def delete_player_by_id(self, player_id: str):
        '''Delete a Player'''

        self.user_business.delete_user_by_id(player_id, role=Roles.PLAYER)
        return SuccessMessage(status=StatusCodes.OK, message=Message.PLAYER_DELETED).message_info

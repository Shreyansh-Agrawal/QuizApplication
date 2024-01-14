'''Controllers for Operations related to Users: SuperAdmin, Admin, Player'''

import logging
from typing import Dict, List, Tuple

import mysql.connector

from config.message_prompts import DisplayMessage, Headers, LogMessage, ErrorMessage
from config.queries import Queries
from models.users.admin import Admin
from utils.custom_error import LoginError

logger = logging.getLogger(__name__)


class User:
    '''User class for user management'''

    def __init__(self, database) -> None:
        self.db = database

    def get_player_scores_by_username(self, username: str) -> List[Tuple]:
        '''Return user's scores'''

        data = self.db.read(Queries.GET_PLAYER_SCORES_BY_USERNAME, (username, ))
        return data

    def get_all_users_by_role(self, role: str) -> List[Tuple]:
        '''Return all users with their details'''

        data = self.db.read(Queries.GET_USER_BY_ROLE, (role, ))
        return data

    def create_admin(self, admin_data: Dict) -> None:
        '''Create a new Admin Account'''

        admin = Admin(admin_data)
        try:
            admin.save_to_database()
        except mysql.connector.IntegrityError as e:
            raise LoginError(ErrorMessage.USER_EXISTS_ERROR) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.ADMIN)
        print(DisplayMessage.CREATE_ADMIN_SUCCESS_MSG)

    def delete_user_by_email(self, role: str, email: str) -> None:
        '''Delete a Player'''

        self.db.write(Queries.DELETE_USER_BY_EMAIL, (email, ))
        logger.debug(LogMessage.DELETE_SUCCESS, Headers.PLAYER)
        print(DisplayMessage.DELETE_USER_SUCCESS_MSG.format(user=role.title(), email=email))

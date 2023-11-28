'''Menu for Super Admin'''

import logging

from config.message_prompts import DisplayMessage, Headers, LogMessage, Prompts
from controllers.handlers.user_handler import UserHandler

logger = logging.getLogger(__name__)


class SuperAdminMenu:
    '''SuperAdminMenu class'''

    @classmethod
    def super_admin_menu(cls, username: str) -> None:
        '''Menu for Super Admin'''

        logger.info(LogMessage.RUNNING_USER_MENU, Headers.SUPER_ADMIN)
        print(DisplayMessage.DASHBOARD_MSG.format(user=Headers.SUPER_ADMIN))
        print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))

        user_handler = UserHandler()
        while True:
            user_choice = input(Prompts.SUPER_ADMIN_PROMPTS)

            match user_choice:
                case '1':
                    user_handler.handle_create_admin()
                case '2':
                    user_handler.display_users_by_role(role='admin')
                case '3':
                    user_handler.handle_delete_user_by_email(role='admin')
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

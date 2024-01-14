'''Menu Functions'''

import logging
from typing import Tuple

from config.message_prompts import DisplayMessage, LogMessage, Prompts
from helpers.auth_handler import AuthHandler
from menu.admin_menu import AdminMenu
from menu.player_menu import PlayerMenu
from menu.super_admin_menu import SuperAdminMenu

logger = logging.getLogger(__name__)


class MainMenu:
    '''Main Menu class'''

    @classmethod
    def assign_menu(cls, data: Tuple) -> None:
        '''Assign menu according to the role'''

        logger.info(LogMessage.ASSIGN_MENU)
        username, role, is_password_changed = data

        match role:
            case 'super admin':
                SuperAdminMenu.super_admin_menu(username)
            case 'admin':
                AdminMenu.admin_menu(username, is_password_changed)
            case 'player':
                PlayerMenu.player_menu(username)
            case _:
                print(DisplayMessage.INVALID_ROLE_MSG, role)


    @classmethod
    def auth_menu(cls) -> None:
        '''Menu for Login / Sign Up'''

        logger.info(LogMessage.RUNNING_AUTH_MENU)
        print(DisplayMessage.APP_WELCOME_MSG)
        auth_handler = AuthHandler()

        while True:
            user_choice = input(Prompts.AUTH_PROMPTS)

            match user_choice:
                case '1':
                    data = auth_handler.handle_login()
                    if not data:
                        continue
                    cls.assign_menu(data)
                case '2':
                    username = auth_handler.handle_signup()
                    if not username:
                        continue
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

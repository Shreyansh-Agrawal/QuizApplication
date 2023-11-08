'''Menu Functions'''

import logging

from config.display_menu import Prompts
from config.display_menu import DisplayMessage
from controllers.handlers import auth_handler as AuthHandler
from controllers.handlers import menu_handler as MenuHandler
from controllers.handlers import quiz_handler as QuizHandler
from controllers.handlers import user_handler as UserHandler

logger = logging.getLogger(__name__)


def super_admin_menu(username: str) -> None:
    '''Menu for Super Admin'''

    logger.info('Running Super Admin Menu')
    print(DisplayMessage.SUPER_ADMIN_MSG)
    print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))

    while True:
        user_choice = input(Prompts.SUPER_ADMIN_PROMPTS)

        match user_choice:
            case '1':
                UserHandler.handle_create_admin()
            case '2':
                UserHandler.display_users_by_role(role='admin')
            case '3':
                UserHandler.handle_delete_user_by_email(role='admin')
            case 'q':
                break
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)


def admin_menu(username: str, is_password_changed: int) -> None:
    '''Menu for Admin'''

    logger.info('Running Admin Menu')
    print(DisplayMessage.ADMIN_MSG)
    print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))

    AuthHandler.handle_first_login(username, is_password_changed)

    while True:
        user_choice = input(Prompts.ADMIN_PROMPTS)

        match user_choice:
            case '1':
                print(DisplayMessage.MANAGE_USERS_MSG)
                MenuHandler.manage_users_menu()
            case '2':
                print(DisplayMessage.MANAGE_QUIZ_MSG)
                MenuHandler.manage_quizzes_menu(username)
            case 'q':
                break
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)


def user_menu(username: str) -> None:
    '''Menu for User'''

    logger.info('Running User Menu')
    print(DisplayMessage.USER_MSG)
    print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))

    while True:
        user_choice = input(Prompts.USER_PROMPTS)

        match user_choice:
            case '1':
                QuizHandler.handle_start_quiz(username)
            case '2':
                QuizHandler.display_leaderboard()
            case '3':
                UserHandler.display_user_score(username)
            case 'q':
                break
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)


def assign_menu(data) -> None:
    '''Assign menu according to the role'''

    logger.info('Assigning menu according to the role')
    username, role, is_password_changed = data

    match role:
        case 'super admin':
            super_admin_menu(username)
        case 'admin':
            admin_menu(username, is_password_changed)
        case 'user':
            user_menu(username)
        case _:
            print(DisplayMessage.INVALID_ROLE_MSG, role)


def start() -> None:
    '''Menu for Login / Sign Up'''

    logger.info('Running start()')
    print(DisplayMessage.APP_WELCOME_MSG)

    while True:
        user_choice = input(Prompts.AUTH_PROMPTS)

        match user_choice:
            case '1':
                data = AuthHandler.handle_login()
                if not data:
                    continue
                assign_menu(data)
            case '2':
                username = AuthHandler.handle_signup()
                if not username:
                    continue
                user_menu(username)
            case 'q':
                break
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)

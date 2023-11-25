'''Menu Functions'''

import logging

from config.display_menu import DisplayMessage, Headers, LogMessage, Prompts
from controllers.handlers import auth_handler as AuthHandler
from controllers.handlers import menu_handler as MenuHandler
from controllers.handlers import quiz_handler as QuizHandler
from controllers.handlers import user_handler as UserHandler

logger = logging.getLogger(__name__)


def super_admin_menu(username: str) -> None:
    '''Menu for Super Admin'''

    logger.info(LogMessage.RUNNING_USER_MENU, Headers.SUPER_ADMIN)
    print(DisplayMessage.DASHBOARD_MSG.format(user=Headers.SUPER_ADMIN))
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

    logger.info(LogMessage.RUNNING_USER_MENU, Headers.ADMIN)
    print(DisplayMessage.DASHBOARD_MSG.format(user=Headers.ADMIN))
    print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))

    AuthHandler.handle_first_login(username, is_password_changed)

    while True:
        user_choice = input(Prompts.ADMIN_PROMPTS)

        match user_choice:
            case '1':
                print(DisplayMessage.MANAGE_PLAYERS_MSG)
                MenuHandler.manage_players_menu()
            case '2':
                print(DisplayMessage.MANAGE_QUIZ_MSG)
                MenuHandler.manage_quizzes_menu(username)
            case 'q':
                break
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)


def player_menu(username: str) -> None:
    '''Menu for Player'''

    logger.info(LogMessage.RUNNING_USER_MENU, Headers.PLAYER)
    print(DisplayMessage.DASHBOARD_MSG.format(user=Headers.PLAYER))
    print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))

    while True:
        user_choice = input(Prompts.PLAYER_PROMPTS)

        match user_choice:
            case '1':
                QuizHandler.handle_start_quiz(username)
            case '2':
                QuizHandler.display_leaderboard()
            case '3':
                UserHandler.display_player_score(username)
            case 'q':
                break
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)


def assign_menu(data) -> None:
    '''Assign menu according to the role'''

    logger.info(LogMessage.ASSIGN_MENU)
    username, role, is_password_changed = data

    match role:
        case 'super admin':
            super_admin_menu(username)
        case 'admin':
            admin_menu(username, is_password_changed)
        case 'player':
            player_menu(username)
        case _:
            print(DisplayMessage.INVALID_ROLE_MSG, role)


def start() -> None:
    '''Menu for Login / Sign Up'''

    logger.info(LogMessage.RUNNING_START)
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
                player_menu(username)
            case 'q':
                break
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)

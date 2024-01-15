'''Menu for Admin'''

import logging

from config.message_prompts import DisplayMessage, Headers, LogMessage, Prompts
from helpers.auth_handler import AuthHandler
from helpers.quiz_handler import QuizHandler
from helpers.user_handler import UserHandler
from utils.quiz_data_loader import load_quiz_data
from utils.custom_error import DataNotFoundError

logger = logging.getLogger(__name__)


class AdminMenu:
    '''Admin Menu class'''

    @classmethod
    def admin_menu(cls, username: str, is_password_changed: int) -> None:
        '''Menu for Admin'''

        logger.info(LogMessage.RUNNING_USER_MENU, Headers.ADMIN)
        print(DisplayMessage.DASHBOARD_MSG.format(user=Headers.ADMIN))
        print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))

        AuthHandler().handle_first_login(username, is_password_changed)
        while True:
            user_choice = input(Prompts.ADMIN_PROMPTS)

            match user_choice:
                case '1':
                    print(DisplayMessage.MANAGE_PLAYERS_MSG)
                    cls.manage_players_menu()
                case '2':
                    print(DisplayMessage.MANAGE_QUIZ_MSG)
                    cls.manage_quizzes_menu(username)
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

    @classmethod
    def manage_quizzes_menu(cls, username: str) -> None:
        '''Admin: manage quizzes menu'''

        logger.info(LogMessage.RUNNING_ADMIN_MENU, Headers.QUIZZES)
        while True:
            user_sub_choice = input(Prompts.ADMIN_MANAGE_QUIZZES_PROMPTS)

            match user_sub_choice:
                case '1':
                    print(DisplayMessage.MANAGE_CATEGORIES_MSG)
                    cls.manage_categories_menu(username)
                case '2':
                    print(DisplayMessage.MANAGE_QUES_MSG)
                    cls.manage_questions_menu(username)
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

    @classmethod
    def manage_players_menu(cls) -> None:
        '''Admin: manage players menu'''

        logger.info(LogMessage.RUNNING_ADMIN_MENU, Headers.PLAYER)
        user_handler = UserHandler()
        while True:
            user_sub_choice = input(Prompts.ADMIN_MANAGE_PLAYER_PROMPTS)

            match user_sub_choice:
                case '1':
                    user_handler.display_users_by_role(role='player')
                case '2':
                    user_handler.handle_delete_user_by_email(role='player')
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

    @classmethod
    def manage_categories_menu(cls, username: str) -> None:
        '''Admin: manage categories menu'''

        logger.info(LogMessage.RUNNING_ADMIN_MENU, Headers.CATEGORIES)
        quiz_handler = QuizHandler()
        while True:
            user_sub_choice = input(Prompts.ADMIN_MANAGE_CATEGORIES_PROMPTS)

            match user_sub_choice:
                case '1':
                    try:
                        quiz_handler.display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
                    except DataNotFoundError as e:
                        logger.exception(e)
                        print(e)
                        continue
                case '2':
                    quiz_handler.handle_create_category(created_by=username)
                case '3':
                    quiz_handler.handle_update_category()
                case '4':
                    quiz_handler.handle_delete_category()
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

    @classmethod
    def manage_questions_menu(cls, username: str) -> None:
        '''Admin: manage questions menu'''

        logger.info(LogMessage.RUNNING_ADMIN_MENU, Headers.QUES)
        quiz_handler = QuizHandler()
        while True:
            user_sub_choice = input(Prompts.ADMIN_MANAGE_QUESTIONS_PROMPTS)

            match user_sub_choice:
                case '1':
                    quiz_handler.display_all_questions()
                case '2':
                    quiz_handler.display_questions_by_category()
                case '3':
                    quiz_handler.handle_create_question(created_by=username)
                case '4':
                    load_quiz_data(admin_username=username)
                    print(DisplayMessage.LOAD_QUES_MSG)
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

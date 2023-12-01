'''Menu for Player'''

import logging

from config.message_prompts import DisplayMessage, Headers, LogMessage, Prompts
from controllers.handlers.quiz_handler import QuizHandler
from controllers.handlers.user_handler import UserHandler

logger = logging.getLogger(__name__)


class PlayerMenu:
    '''Player Menu class'''

    @classmethod
    def player_menu(cls, username: str) -> None:
        '''Menu for Player'''

        logger.info(LogMessage.RUNNING_USER_MENU, Headers.PLAYER)
        print(DisplayMessage.DASHBOARD_MSG.format(user=Headers.PLAYER))
        print(DisplayMessage.USER_WELCOME_MSG.format(user=username.lower()))
        quiz_handler = QuizHandler()
        user_handler = UserHandler()

        while True:
            user_choice = input(Prompts.PLAYER_PROMPTS)

            match user_choice:
                case '1':
                    quiz_handler.handle_start_quiz(username)
                case '2':
                    quiz_handler.display_leaderboard()
                case '3':
                    user_handler.display_player_score(username)
                case 'q':
                    break
                case _:
                    print(DisplayMessage.WRONG_INPUT_MSG)

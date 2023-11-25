'''Handlers related to generic users: Super Admin, Admin, Player'''

import logging

from config.message_prompts import DisplayMessage, Headers, LogMessage
from controllers import user_controller as UserController
from utils.custom_error import DataNotFoundError, LoginError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


def display_users_by_role(role: str) -> None:
    '''Display users on console by role'''

    logger.debug(LogMessage.DISPLAY_ALL_ENTITY, role)
    data = UserController.get_all_users_by_role(role)

    if not data:
        print(DisplayMessage.USER_NOT_FOUND_MSG.format(user=role))
        return

    print(DisplayMessage.DISPLAY_USERS_MSG.format(user=role.title()))
    pretty_print(
        data=data,
        headers=(Headers.USERNAME, Headers.NAME, Headers.EMAIL, Headers.REG_DATE)
    )


def display_player_score(username: str) -> None:
    '''Display past scores of player'''

    logger.debug(LogMessage.DISPLAY_QUIZ_SCORE, username)
    data = UserController.get_player_scores_by_username(username)

    if not data:
        print(DisplayMessage.QUIZ_DATA_NOT_FOUND_MSG)
        return

    print(DisplayMessage.SCORE_DATA_MSG)
    pretty_print(data=data, headers=(Headers.TIME, Headers.SCORE))

    scores = [scores[1] for scores in data]
    print(DisplayMessage.HIGHEST_SCORE_MSG.format(score=max(scores)))


def handle_create_admin() -> None:
    '''Handle admin profile creation'''

    try:
        UserController.create_admin()
    except LoginError as e:
        logger.warning(e)
        print(e)


def handle_delete_user_by_email(role: str) -> None:
    '''Handle user deletion by role'''

    try:
        UserController.delete_user_by_email(role)
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)

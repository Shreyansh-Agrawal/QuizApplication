'''Handlers related to generic users: Super Admin, Admin, Player'''

import logging
import random
import string

from config.message_prompts import DisplayMessage, Headers, LogMessage
from config.regex_patterns import RegexPattern
from controllers.user_controller import UserController
from utils import validations
from utils.custom_error import DataNotFoundError, LoginError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


def display_users_by_role(role: str) -> None:
    '''Display users on console by role'''

    logger.debug(LogMessage.DISPLAY_ALL_ENTITY, role)
    data = UserController().get_all_users_by_role(role)

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
    data = UserController().get_player_scores_by_username(username)

    if not data:
        print(DisplayMessage.QUIZ_DATA_NOT_FOUND_MSG)
        return

    print(DisplayMessage.SCORE_DATA_MSG)
    pretty_print(data=data, headers=(Headers.TIME, Headers.SCORE))

    scores = [scores[1] for scores in data]
    print(DisplayMessage.HIGHEST_SCORE_MSG.format(score=max(scores)))


def handle_create_admin() -> None:
    '''Handle admin profile creation'''

    logger.debug(LogMessage.CREATE_ENTITY, Headers.ADMIN)
    print(DisplayMessage.CREATE_ADMIN_MSG)

    admin_data = {}
    admin_data['name'] = validations.regex_validator(
        prompt='Enter admin name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    ).title()
    admin_data['email'] = validations.regex_validator(
        prompt='Enter admin email: ',
        regex_pattern=RegexPattern.EMAIL_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)
    )
    admin_data['username'] = validations.regex_validator(
        prompt='Create admin username: ',
        regex_pattern=RegexPattern.USERNAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.USERNAME)
    )
    characters = string.ascii_letters + string.digits + '@#$&'
    password = ''.join(random.choice(characters) for _ in range(6))
    admin_data['password'] = password

    try:
        UserController().create_admin(admin_data)
    except LoginError as e:
        logger.warning(e)
        print(e)


def handle_delete_user_by_email(role: str) -> None:
    '''Handle user deletion by role'''

    try:
        data = UserController().get_all_users_by_role(role)
        if not data:
            raise DataNotFoundError(f'No {role} Currently!')

        logger.debug(LogMessage.DELETE_ENTITY, {role.title()})
        print(DisplayMessage.DELETE_USER_MSG.format(user=role.title()))
        pretty_print(data=data, headers=(Headers.USERNAME, Headers.NAME, Headers.EMAIL, Headers.REG_DATE))

        email = validations.regex_validator(
            prompt=f'\nEnter {role.title()} Email: ',
            regex_pattern=RegexPattern.EMAIL_PATTERN,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)
        )
        for data in data:
            if data[2] == email:
                break
        else:
            print(DisplayMessage.DELETE_USER_FAIL_MSG.format(user=role.title()))
            return

        UserController().delete_user_by_email(role, email)
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)

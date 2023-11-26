'''Handlers related to Authentication'''

import logging
from typing import List, Tuple

from config.message_prompts import DisplayMessage, Headers, LogMessage, Prompts
from config.queries import Queries
from config.regex_patterns import RegexPattern
from controllers.auth_controller import AuthController
from database.database_access import DatabaseAccess as DAO
from utils import validations
from utils.custom_error import LoginError
from utils.password_hasher import hash_password

logger = logging.getLogger(__name__)


def handle_login() -> List[Tuple]:
    '''Handles Login'''

    logger.debug(LogMessage.LOGIN_INITIATED)
    print(DisplayMessage.LOGIN_MSG)
    attempts_remaining = Prompts.ATTEMPT_LIMIT

    while True:
        # validating credentials even during login to prevent any Injections
        username = validations.regex_validator(
            prompt='Enter your username: ',
            regex_pattern=RegexPattern.USERNAME_PATTERN,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.USERNAME)
        )
        password = validations.validate_password(prompt='Enter your password: ')

        data = AuthController().login(username, password)
        if data:
            break

        attempts_remaining -= 1
        print(DisplayMessage.REMAINING_ATTEMPTS_MSG.format(count=attempts_remaining))

        if attempts_remaining == 0:
            print(DisplayMessage.LOGIN_ATTEMPTS_EXHAUST_MSG)
            logger.debug(LogMessage.LOGIN_ATTEMPTS_EXHAUSTED)
            return None

    logger.debug(LogMessage.LOGIN_SUCCESS)
    return data


def handle_signup() -> str:
    '''Handles Signup'''

    logger.debug(LogMessage.SIGNUP_INITIATED)
    print(DisplayMessage.SIGNUP_MSG)

    player_data = {}
    player_data['name'] = validations.regex_validator(
        prompt='Enter your name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    ).title()
    player_data['email'] = validations.regex_validator(
        prompt='Enter your email: ',
        regex_pattern=RegexPattern.EMAIL_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)
    )
    player_data['username'] = validations.regex_validator(
        prompt='Create your username: ',
        regex_pattern=RegexPattern.USERNAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.USERNAME)
    )
    password = validations.validate_password(prompt='Create your password: ')
    confirm_password = ''

    while True:
        confirm_password =  validations.validate_password(prompt='Confirm Password: ')
        if password != confirm_password:
            print(DisplayMessage.CONFIRM_PSWD_FAIL_MSG)
        else:
            break

    player_data['password'] = confirm_password
    try:
        username = AuthController().signup(player_data)
    except LoginError as e:
        print(e)
        logger.warning(e)
        return None

    logger.debug(LogMessage.SIGNUP_SUCCESS)
    print(DisplayMessage.REDIRECT_MSG)
    return username


def handle_first_login(username: str, is_password_changed: int) -> None:
    '''Checks Admin's First Login'''

    if not is_password_changed:
        print(DisplayMessage.CHANGE_PSWD_MSG)
        logger.debug(LogMessage.CHANGE_DEFAULT_ADMIN_PSW)

        new_password = validations.validate_password(prompt='Enter New Password: ')
        confirm_password = ''

        while True:
            confirm_password =  validations.validate_password(prompt='Confirm Password: ')
            if new_password != confirm_password:
                print(DisplayMessage.CONFIRM_PSWD_FAIL_MSG)
            else:
                break

        hashed_password = hash_password(confirm_password)
        is_password_changed = 1

        DAO.write_to_database(
            Queries.UPDATE_ADMIN_PASSWORD_BY_USERNAME,
            (hashed_password, is_password_changed, username)
        )

        logger.debug(LogMessage.CHANGE_DEFAULT_ADMIN_PSW_SUCCESS)
        print(DisplayMessage.CHANGE_PSWD_SUCCESS_MSG)

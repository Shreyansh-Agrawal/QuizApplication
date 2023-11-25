'''Controllers for Operations related to Authentication'''

import hashlib
import logging
import sqlite3
from typing import Tuple

from config.message_prompts import DisplayMessage, Headers, LogMessage
from config.queries import Queries
from config.regex_patterns import RegexPattern
from database.database_access import DatabaseAccess as DAO
from models.user import Player
from utils import validations
from utils.custom_error import LoginError

logger = logging.getLogger(__name__)


def login() -> Tuple:
    '''Method for user login'''

    logger.debug(LogMessage.LOGIN_INITIATED)

    # validating credentials even during login to prevent any Injections
    username = validations.regex_validator(
        prompt='Enter your username: ',
        regex_pattern=RegexPattern.USERNAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.USERNAME)
    )
    password = validations.validate_password(prompt='Enter your password: ')
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    user_data = DAO.read_from_database(Queries.GET_CREDENTIALS_BY_USERNAME, (username, ))
    if not user_data:
        print(DisplayMessage.AUTH_INVALIDATE_MSG)
        return ()

    user_password, role, is_password_changed = user_data[0]

    if not is_password_changed and user_password != password:
        print(DisplayMessage.AUTH_INVALIDATE_MSG)
        return ()

    if is_password_changed and user_password != hashed_password:
        print(DisplayMessage.AUTH_INVALIDATE_MSG)
        return ()

    logger.debug(LogMessage.LOGIN_SUCCESS)
    print(DisplayMessage.LOGIN_SUCCESS_MSG)

    return (username, role, is_password_changed)


def signup() -> str:
    '''Method for signup, only for player'''

    logger.debug(LogMessage.SIGNUP_INITIATED)

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

    hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
    player_data['password'] = hashed_password

    player = Player(player_data)

    try:
        player.save_to_database()
    except sqlite3.IntegrityError as e:
        raise LoginError(
            'User already exists! Login or Sign Up with different credentials...'
        ) from e

    logger.debug(LogMessage.SIGNUP_SUCCESS)
    print(DisplayMessage.SIGNUP_SUCCESS_MSG)

    return player_data['username']

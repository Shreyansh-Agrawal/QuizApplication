'''Controllers for Operations related to Authentication'''

import hashlib
import logging
import sqlite3
from typing import Tuple

from config.display_menu import DisplayMessage, Headers
from config.queries import Queries
from config.regex_patterns import RegexPattern
from database.database_access import DatabaseAccess as DAO
from models.user import User
from utils import validations
from utils.custom_error import LoginError

logger = logging.getLogger(__name__)


def login() -> Tuple:
    '''Method for user login'''

    logger.debug('Login Initiated')

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

    logger.debug('Login Successful')
    print(DisplayMessage.LOGIN_SUCCESS_MSG)

    return (username, role, is_password_changed)


def signup() -> str:
    '''Method for signup, only for user'''

    logger.debug('Signup Initiated')

    user_data = {}
    user_data['name'] = validations.regex_validator(
        prompt='Enter your name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    )
    user_data['email'] = validations.regex_validator(
        prompt='Enter your email: ',
        regex_pattern=RegexPattern.EMAIL_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)
    )
    user_data['username'] = validations.regex_validator(
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
    user_data['password'] = hashed_password

    user = User(user_data)

    try:
        user.save_user_to_database()
    except sqlite3.IntegrityError as e:
        raise LoginError(
            'User already exists! Login or Sign Up with different credentials...'
        ) from e

    logger.debug('Signup Successful')
    print(DisplayMessage.SIGNUP_SUCCESS_MSG)

    return user_data['username']

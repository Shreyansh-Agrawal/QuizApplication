'''Handlers related to Authentication'''

import hashlib
import logging
from typing import List, Tuple

from config.display_menu import DisplayMessage, Prompts, LogMessage
from config.queries import Queries
from controllers import auth_controller as Authenticate
from database.database_access import DatabaseAccess as DAO
from utils import validations
from utils.custom_error import LoginError

logger = logging.getLogger(__name__)


def handle_login() -> List[Tuple]:
    '''Handles Login'''

    logger.debug(LogMessage.LOGIN_INITIATED)
    print(DisplayMessage.LOGIN_MSG)

    attempts_remaining = Prompts.ATTEMPT_LIMIT

    data = Authenticate.login()
    while not data:
        attempts_remaining -= 1
        print(DisplayMessage.REMAINING_ATTEMPTS_MSG.format(count=attempts_remaining))

        if attempts_remaining == 0:
            print(DisplayMessage.LOGIN_ATTEMPTS_EXHAUST_MSG)
            logger.debug(LogMessage.LOGIN_ATTEMPTS_EXHAUSTED)
            return None

        data = Authenticate.login()

    logger.debug(LogMessage.LOGIN_SUCCESS)
    return data


def handle_signup() -> str:
    '''Handles Signup'''

    logger.debug(LogMessage.SIGNUP_INITIATED)
    print(DisplayMessage.SIGNUP_MSG)

    try:
        username = Authenticate.signup()
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

        hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
        is_password_changed = 1

        DAO.write_to_database(
            Queries.UPDATE_ADMIN_PASSWORD_BY_USERNAME,
            (hashed_password, is_password_changed, username)
        )

        logger.debug(LogMessage.CHANGE_DEFAULT_ADMIN_PSW_SUCCESS)
        print(DisplayMessage.CHANGE_PSWD_SUCCESS_MSG)

'''Controllers for Operations related to Users: SuperAdmin, Admin, User'''

import logging
import sqlite3
from typing import List, Tuple

from password_generator import PasswordGenerator

from config.display_menu import DisplayMessage, Headers
from config.queries import Queries
from config.regex_patterns import RegexPattern
from database.database_access import DatabaseAccess as DAO
from models.user import Admin
from utils import validations
from utils.custom_error import DataNotFoundError, LoginError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


def get_user_scores_by_username(username: str) -> List[Tuple]:
    '''Return user's scores'''

    data = DAO.read_from_database(Queries.GET_USER_SCORES_BY_USERNAME, (username, ))
    return data


def get_all_users_by_role(role: str) -> List[Tuple]:
    '''Return all users with their details'''

    data = DAO.read_from_database(Queries.GET_USER_BY_ROLE, (role, ))
    return data


def create_admin() -> None:
    '''Create a new Admin Account'''

    logger.debug('Creating Admin')
    print(DisplayMessage.CREATE_ADMIN_MSG)

    admin_data = {}
    admin_data['name'] = validations.regex_validator(
        prompt='Enter admin name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    )
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
    pwo = PasswordGenerator()
    pwo.excludeschars = "!@#$%^&*()./?'"
    password = pwo.non_duplicate_password(7)
    admin_data['password'] = password

    admin = Admin(admin_data)

    try:
        admin.save_user_to_database()
    except sqlite3.IntegrityError as e:
        raise LoginError('\nUser already exists! Try with different credentials...') from e

    logger.debug('Admin created')
    print(DisplayMessage.CREATE_ADMIN_SUCCESS_MSG)


def delete_user_by_email(role: str) -> None:
    '''Delete a User'''

    data = get_all_users_by_role(role)
    if not data:
        raise DataNotFoundError(f'No {role} Currently!')

    logger.debug('Deleting %s', {role.title()})
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

    DAO.write_to_database(Queries.DELETE_USER_BY_EMAIL, (email, ))

    logger.debug('User deleted')
    print(DisplayMessage.DELETE_USER_SUCCESS_MSG.format(user=role.title(), email=email))

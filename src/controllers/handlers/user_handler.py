'''Handlers related to generic users: Super Admin, Admin, Player'''

import logging
import random
import string

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage, Prompts
from config.regex_patterns import RegexPattern
from controllers.user_controller import UserController
from utils import validations
from utils.custom_error import DataNotFoundError, LoginError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


class UserHandler:
    '''UserHandler class containing methods for managing users - Admin and Player'''

    def __init__(self) -> None:
        self.user_controller = UserController()

    def display_users_by_role(self, role: str) -> None:
        '''Display users on console by role'''

        logger.debug(LogMessage.DISPLAY_ALL_ENTITY, role)
        data = self.user_controller.get_all_users_by_role(role)

        if not data:
            print(DisplayMessage.USER_NOT_FOUND_MSG.format(user=role))
            return

        print(DisplayMessage.DISPLAY_USERS_MSG.format(user=role.title()))
        pretty_print(
            data=data,
            headers=(Headers.USERNAME, Headers.NAME, Headers.EMAIL, Headers.REG_DATE)
        )

    def display_player_score(self, username: str) -> None:
        '''Display past scores of player'''

        logger.debug(LogMessage.DISPLAY_QUIZ_SCORE, username)
        data = self.user_controller.get_player_scores_by_username(username)

        if not data:
            print(DisplayMessage.QUIZ_DATA_NOT_FOUND_MSG)
            return

        print(DisplayMessage.SCORE_DATA_MSG)
        pretty_print(data=data, headers=(Headers.TIME, Headers.SCORE))
        scores = [scores[1] for scores in data]
        print(DisplayMessage.HIGHEST_SCORE_MSG.format(score=max(scores)))

    def handle_create_admin(self) -> None:
        '''Handle admin profile creation'''

        logger.debug(LogMessage.CREATE_ENTITY, Headers.ADMIN)
        print(DisplayMessage.CREATE_ADMIN_MSG)

        admin_data = {}
        admin_data['name'] = validations.regex_validator(
            prompt=Prompts.ADMIN_NAME_PROMPT,
            regex_pattern=RegexPattern.NAME_PATTERN,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
        ).title()
        admin_data['email'] = validations.regex_validator(
            prompt=Prompts.ADMIN_EMAIL_PROMPT,
            regex_pattern=RegexPattern.EMAIL_PATTERN,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)
        )
        admin_data['username'] = validations.regex_validator(
            prompt=Prompts.CREATE_USERNAME_PROMPT,
            regex_pattern=RegexPattern.USERNAME_PATTERN,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.USERNAME)
        )
        characters = string.ascii_letters + string.digits + '@#$&'
        password = ''.join(random.choice(characters) for _ in range(6))
        admin_data['password'] = password

        try:
            self.user_controller.create_admin(admin_data)
        except LoginError as e:
            logger.warning(e)
            print(e)

    def handle_delete_user_by_email(self, role: str) -> None:
        '''Handle user deletion by role'''

        try:
            data = self.user_controller.get_all_users_by_role(role)
            if not data:
                raise DataNotFoundError(ErrorMessage.NO_ROLE_ERROR.format(role=role))

            logger.debug(LogMessage.DELETE_ENTITY, {role.title()})
            print(DisplayMessage.DELETE_USER_MSG.format(user=role.title()))
            pretty_print(data=data, headers=(Headers.USERNAME, Headers.NAME, Headers.EMAIL, Headers.REG_DATE))

            email = validations.regex_validator(
                prompt=Prompts.USER_EMAIL_PROMPT.format(role=role.title()),
                regex_pattern=RegexPattern.EMAIL_PATTERN,
                error_msg=DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)
            )
            for data in data:
                if data[2] == email:
                    break
            else:
                print(DisplayMessage.DELETE_USER_FAIL_MSG.format(user=role.title()))
                return

            self.user_controller.delete_user_by_email(role, email)
        except DataNotFoundError as e:
            logger.warning(e)
            print(e)

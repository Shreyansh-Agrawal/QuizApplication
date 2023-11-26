'''Handlers related to Quiz'''

import logging
from typing import Tuple

from config.message_prompts import DisplayMessage, Headers, LogMessage, Prompts
from config.queries import Queries
from config.regex_patterns import RegexPattern
from controllers.helpers import quiz_helper as QuizHelper
from controllers.helpers import start_quiz_helper as StartQuizHelper
from controllers.quiz_controller import QuizController
from database.database_access import DatabaseAccess as DAO
from utils import validations
from utils.custom_error import DataNotFoundError, DuplicateEntryError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


def display_categories(role: str, header: Tuple) -> None:
    '''Display Categories on Console'''

    logger.debug(LogMessage.DISPLAY_ALL_ENTITY, Headers.CATEGORY)
    data = QuizHelper.get_all_categories()

    if not data:
        raise DataNotFoundError('No Category Added!')

    print(DisplayMessage.CATEGORIES_MSG)

    if role == 'player':
        data = [(tup[0], ) for tup in data]

    pretty_print(data=data, headers=header)


def display_all_questions() -> None:
    '''Display All Questions on Console'''

    logger.debug(LogMessage.DISPLAY_ALL_ENTITY, Headers.QUES)
    data = QuizController().get_all_questions()

    if not data:
        logger.debug(LogMessage.QUES_DATA_NOT_FOUND)
        print(DisplayMessage.QUES_NOT_FOUND_MSG)
        return

    print(DisplayMessage.QUES_MSG)
    pretty_print(
        data=data,
        headers=(Headers.CATEGORY, Headers.QUES, Headers.QUES_TYPE, Headers.ANS, Headers.CREATED_BY)
    )


def display_questions_by_category() -> None:
    '''Display Questions by Category on Console'''

    logger.debug(LogMessage.DISPLAY_QUES_BY_CATEGORY)
    try:
        display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
        categories = QuizHelper.get_all_categories()

        user_choice = validations.regex_validator(
            prompt='Choose a Category: ',
            regex_pattern=RegexPattern.NUMERIC_PATTERN,
            error_msg=DisplayMessage.INVALID_CHOICE
        )
        user_choice = int(user_choice)

        if user_choice > len(categories) or user_choice-1 < 0:
            raise DataNotFoundError('No such Category! Please choose from above!!')
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
        return

    category_name = categories[user_choice-1][0]
    print(DisplayMessage.DISPLAY_QUES_IN_A_CATEGORY_MSG.format(name=category_name))
    data = QuizController().get_questions_by_category(category_name)

    if not data:
        print(DisplayMessage.QUES_NOT_FOUND_MSG)
        return

    pretty_print(
        data=data,
        headers=(Headers.QUES, Headers.QUES_TYPE, Headers.ANS, Headers.CREATED_BY)
    )


def display_leaderboard() -> None:
    '''Display Leaderboard on Console'''

    data = QuizController().get_leaderboard()

    if not data:
        logger.debug(LogMessage.LEADERBOARD_DATA_NOT_FOUND)
        print(DisplayMessage.QUIZ_DATA_NOT_FOUND_MSG)
        return

    print(DisplayMessage.LEADERBOARD_MSG)
    pretty_print(data=data, headers=(Headers.USERNAME, Headers.SCORE, Headers.TIME))


def handle_start_quiz(username: str) -> None:
    '''Handler for starting Quiz'''

    logger.debug(LogMessage.START_QUIZ, username)

    while True:
        print('\n-----SELECT QUIZ MODE-----')
        quiz_mode = input(Prompts.SELECT_MODE_PROMPTS)

        match quiz_mode:
            case '1':
                try:
                    category = StartQuizHelper.select_category()
                    QuizController().start_quiz(username, category)
                except DataNotFoundError as e:
                    logger.warning(e)
                    print(e)
                    return
            case '2':
                try:
                    QuizController().start_quiz(username)
                except DataNotFoundError as e:
                    logger.warning(e)
                    print(e)
                    return
            case 'q':
                return
            case _:
                print(DisplayMessage.WRONG_INPUT_MSG)


def handle_create_category(created_by: str) -> None:
    '''Handler for creating category'''

    try:
        display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
    admin_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (created_by, ))
    admin_id = admin_data[0][0]
    print(DisplayMessage.CREATE_CATEGORY_MSG)

    category_data = {}
    category_data['admin_id'] = admin_id
    category_data['admin_username'] = created_by
    category_data['category_name'] = validations.regex_validator(
        prompt='Enter New Category Name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    ).title()
    try:
        QuizController().create_category(category_data)
    except DuplicateEntryError as e:
        logger.warning(e)
        print(e)


def handle_create_question(created_by: str) -> None:
    '''Handler for creating question'''

    try:
        display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
        QuizController().create_question(created_by)
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
        return
    except DuplicateEntryError as e:
        logger.warning(e)
        print(e)
        return


def handle_update_category() -> None:
    '''Handler for updating a category'''

    try:
        display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
        categories = QuizHelper.get_all_categories()

        print(DisplayMessage.UPDATE_CATEGORY_MSG)

        user_choice = validations.regex_validator(
            prompt='Choose a Category: ',
            regex_pattern=RegexPattern.NUMERIC_PATTERN,
            error_msg=DisplayMessage.INVALID_CHOICE
        )
        user_choice = int(user_choice)
        if user_choice > len(categories) or user_choice-1 < 0:
            raise DataNotFoundError('No such Category! Please choose from above!!')
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
        return

    old_category_name = categories[user_choice-1][0]
    new_category_name = validations.regex_validator(
        prompt='Enter updated category name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    ).title()
    try:
        QuizController().update_category_by_name(old_category_name, new_category_name)
    except DuplicateEntryError as e:
        logger.warning(e)
        print(e)
        return

def handle_delete_category() -> None:
    '''Handler for deleting a category'''

    try:
        display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
        categories = QuizHelper.get_all_categories()

        logger.debug(LogMessage.DELETE_ENTITY, Headers.CATEGORY)
        print(DisplayMessage.DELETE_CATEGORY_MSG)

        user_choice = validations.regex_validator(
            prompt='Choose a Category: ',
            regex_pattern=RegexPattern.NUMERIC_PATTERN,
            error_msg=DisplayMessage.INVALID_CHOICE
        )
        user_choice = int(user_choice)
        if user_choice > len(categories) or user_choice-1 < 0:
            raise DataNotFoundError('No such Category! Please choose from above!!')
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
        return

    category_name = categories[user_choice-1][0]

    while True:
        print(DisplayMessage.DELETE_CATEGORY_WARNING_MSG.format(name=category_name))
        confirmation = input('Type "YES" if you wish to continue\nPress any other key to go back: ')
        if confirmation.lower() == 'yes':
            break
        return
    QuizController().delete_category_by_name(category_name)

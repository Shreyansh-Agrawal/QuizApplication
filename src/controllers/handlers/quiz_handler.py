'''Handlers related to Quiz'''

import logging
from typing import Tuple

from config.message_prompts import DisplayMessage, Headers, LogMessage, Prompts
from controllers import quiz_controller as QuizController
from controllers.helpers import quiz_helper as QuizHelper
from controllers.helpers import start_quiz_helper as StartQuizHelper
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
    data = QuizController.get_all_questions()

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
        data = QuizController.get_questions_by_category()
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
        return

    if not data:
        print(DisplayMessage.QUES_NOT_FOUND_MSG)
        return

    pretty_print(
        data=data,
        headers=(Headers.QUES, Headers.QUES_TYPE, Headers.ANS, Headers.CREATED_BY)
    )


def display_leaderboard() -> None:
    '''Display Leaderboard on Console'''

    data = QuizController.get_leaderboard()

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
                    QuizController.start_quiz(username, category)
                except DataNotFoundError as e:
                    logger.warning(e)
                    print(e)
                    return
            case '2':
                try:
                    QuizController.start_quiz(username)
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

    try:
        QuizController.create_category(created_by)
    except DuplicateEntryError as e:
        logger.warning(e)
        print(e)


def handle_create_question(created_by: str) -> None:
    '''Handler for creating question'''

    try:
        display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
        QuizController.create_question(created_by)
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
        QuizController.update_category_by_name()
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
        return


def handle_delete_category() -> None:
    '''Handler for deleting a category'''

    try:
        display_categories(role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY))
        QuizController.delete_category_by_name()
    except DataNotFoundError as e:
        logger.warning(e)
        print(e)
        return

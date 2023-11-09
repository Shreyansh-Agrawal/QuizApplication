'''Helper functions for Starting Quiz'''

import logging
from datetime import datetime, timezone
from typing import List, Tuple

from config.display_menu import DisplayMessage, Headers
from config.queries import Queries
from config.regex_patterns import RegexPattern
from controllers.helpers import quiz_helper as QuizHelper
from database.database_access import DatabaseAccess as DAO
from utils.custom_error import DataNotFoundError
from utils import validations
from utils.pretty_print import pretty_print


logger = logging.getLogger(__name__)


def get_random_questions() -> List[Tuple]:
    '''Return random questions across all categories'''

    data = DAO.read_from_database(Queries.GET_RANDOM_QUESTIONS)
    return data


def get_random_questions_by_category(category: str) -> List[Tuple]:
    '''Return random questions by category'''

    data = DAO.read_from_database(Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY, (category, ))
    return data


def select_category():
    '''Takes in user input for category'''

    try:
        data = QuizHelper.get_all_categories()
    except DataNotFoundError as e:
        raise e

    categories = [(tup[0], ) for tup in data]
    pretty_print(data=categories, headers=(Headers.CATEGORY, ))
    print(DisplayMessage.QUIZ_START_MSG)

    user_choice = validations.regex_validator(
        prompt='Choose a Category: ',
        regex_pattern=RegexPattern.NUMERIC_PATTERN,
        error_msg=DisplayMessage.INVALID_CHOICE
    )

    user_choice = int(user_choice)
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError(DisplayMessage.CATEGORY_NOT_FOUND_MSG)

    category = categories[user_choice-1][0]

    for data in categories:
        if data[0] == category:
            break
    else:
        raise DataNotFoundError(DisplayMessage.CATEGORY_NOT_FOUND_MSG)

    return category


def display_question(question_no: int, question: str, question_type: str, options_data: List[Tuple]) -> None:
    '''Display question and its options to user'''

    print(f'\n{question_no}) {question}')

    if question_type.lower() == 'mcq':
        options = [option[0] for option in options_data]

        for count, option in enumerate(options, 1):
            print(f'    {count}. {option}')

    elif question_type.lower() == 't/f':
        print(DisplayMessage.TF_OPTION_MSG)


def get_user_response(question_type: str) -> str:
    '''Gets user response according to question type'''

    if question_type.lower() == 'mcq':
        while True:
            user_choice = validations.regex_validator(
                prompt='Choose an option: ',
                regex_pattern=RegexPattern.NUMERIC_PATTERN,
                error_msg=DisplayMessage.INVALID_CHOICE
            )

            user_choice = int(user_choice)
            if user_choice not in range(1, 5):
                print(DisplayMessage.MCQ_WRONG_OPTION_MSG)
                continue
            return user_choice

    elif question_type.lower() == 't/f':
        while True:
            user_choice = validations.regex_validator(
                prompt='Choose an option: ',
                regex_pattern=RegexPattern.NUMERIC_PATTERN,
                error_msg=DisplayMessage.INVALID_CHOICE
            )

            user_choice = int(user_choice)
            match user_choice:
                case 1:
                    return 'true'
                case 2:
                    return 'false'
                case _:
                    print(DisplayMessage.TF_WRONG_OPTION_MSG)
    else:
        user_answer = validations.regex_validator(
            prompt='-> Enter your answer: ',
            regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
        )
        return user_answer


def save_quiz_score(username: str, score: int) -> None:
    '''Saving User's Quiz Score'''

    logger.debug('Saving score for: %s', username)
    user_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    user_id = user_data[0][0]
    score_id = validations.validate_id(entity='score')

    time = datetime.now(timezone.utc) # current utc time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

    DAO.write_to_database(Queries.INSERT_USER_QUIZ_SCORE, (score_id, user_id, score, timestamp))
    logger.debug('Score saved for: %s', username)

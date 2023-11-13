'''Helper functions for Managing Quiz'''

import logging
from typing import Dict, List, Tuple

from config.display_menu import DisplayMessage, Headers, Prompts
from config.queries import Queries
from config.regex_patterns import RegexPattern
from database.database_access import DatabaseAccess as DAO
from models.quiz import Option, Question
from utils import validations
from utils.custom_error import DataNotFoundError

logger = logging.getLogger(__name__)


def get_all_categories() -> List[Tuple]:
    '''Return all Quiz Categories'''

    data = DAO.read_from_database(Queries.GET_ALL_CATEGORIES)
    return data


def get_question_data(username: str) -> Dict:
    '''Takes input of question details'''
    categories = get_all_categories()

    logger.debug('Creating Question')
    print(DisplayMessage.CREATE_QUES_MSG)

    user_choice = validations.regex_validator(
        prompt='Choose a Category: ',
        regex_pattern=RegexPattern.NUMERIC_PATTERN,
        error_msg=DisplayMessage.INVALID_CHOICE
    )

    user_choice = int(user_choice)
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]

    category_id = DAO.read_from_database(Queries.GET_CATEGORY_ID_BY_NAME, (category_name, ))
    admin_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    admin_id = admin_data[0][0]

    question_data = {}
    question_data['category_id'] = category_id[0][0]
    question_data['admin_id'] = admin_id
    question_data['admin_username'] = username
    question_data['question_text'] = validations.regex_validator(
        prompt='Enter Question Text: ',
        regex_pattern=RegexPattern.QUES_TEXT_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.QUES)
    ).title()

    return question_data


def create_option(question_data: Dict) -> Question:
    '''Create options, returns a question object'''

    while True:
        question_type_input = input(Prompts.QUESTION_TYPE_PROMPTS)
        match question_type_input:
            case '1':
                question_data['question_type'] = 'MCQ'
                break
            case '2':
                question_data['question_type'] = 'T/F'
                break
            case '3':
                question_data['question_type'] = 'ONE WORD'
                break
            case _:
                print(DisplayMessage.INVALID_QUES_TYPE_MSG)
                continue

    question = Question(question_data)

    match question_data['question_type']:
        case 'MCQ':
            option_data = {}
            option_data['question_id'] = question.entity_id
            option_data['option_text'] = validations.regex_validator(
                prompt='Enter Answer: ',
                regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
            ).title()
            option_data['is_correct'] = 1
            option = Option(option_data)
            question.add_option(option)

            for _ in range(3):
                option_data['question_id'] = question.entity_id
                option_data['option_text'] = validations.regex_validator(
                    prompt='Enter Other Option: ',
                    regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                    error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
                ).title()
                option_data['is_correct'] = 0
                option = Option(option_data)
                question.add_option(option)
        case 'T/F' | 'ONE WORD':
            option_data = {}
            option_data['question_id'] = question.entity_id
            option_data['option_text'] = validations.regex_validator(
                prompt='Enter Answer: ',
                regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
            ).title()
            option_data['is_correct'] = 1

            option = Option(option_data)
            question.add_option(option)
        case _:
            logger.exception('Invalid Ques Type!')
            return None

    return question

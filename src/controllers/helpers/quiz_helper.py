'''Helper functions for Starting Quiz'''

import logging
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from config.display_menu import Prompts
from config.display_menu import DisplayMessage
from config.queries import Queries
from config.regex_patterns import RegexPattern
from database.database_access import DatabaseAccess as DAO
from models.quiz import Option, Question
from utils import validations

logger = logging.getLogger(__name__)


def create_option(question_data: Dict):
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
            option_data['question_id'] = question.question_id
            option_data['option_text'] = validations.regex_validator(
                prompt='Enter Answer: ',
                regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                error_msg='Invalid option!'
            )
            option_data['is_correct'] = 1
            option = Option(option_data)
            question.add_option(option)

            for _ in range(3):
                option_data['question_id'] = question.question_id
                option_data['option_text'] = validations.regex_validator(
                    prompt='Enter Other Option: ',
                    regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                    error_msg='Invalid option!'
                )
                option_data['is_correct'] = 0
                option = Option(option_data)
                question.add_option(option)
        case 'T/F' | 'ONE WORD':
            option_data = {}
            option_data['question_id'] = question.question_id
            option_data['option_text'] = validations.regex_validator(
                prompt='Enter Answer: ',
                regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                error_msg='Invalid option!'
            )
            option_data['is_correct'] = 1

            option = Option(option_data)
            question.add_option(option)
        case _:
            logger.exception('Invalid Ques Type!')
            return None

    return question


def display_question(question_no: int, question: str, question_type: str, options_data: List[Tuple]):
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
                error_msg='Select a number from above options!'
            )
            if user_choice not in range(1, 5):
                print(DisplayMessage.MCQ_WRONG_OPTION_MSG)
                continue
            return user_choice

    elif question_type.lower() == 't/f':
        while True:
            user_choice = validations.regex_validator(
                prompt='Choose an option: ',
                regex_pattern=RegexPattern.NUMERIC_PATTERN,
                error_msg='Select a number from above options!'
            )
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
            error_msg='Invalid option!'
        )
        return user_answer


def save_quiz_score(username: str, score: int):
    '''Saving User's Quiz Score'''

    logger.debug('Saving score for: %s', username)
    user_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    user_id = user_data[0][0]
    score_id = validations.validate_id(entity='score')

    time = datetime.now(timezone.utc) # current utc time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

    DAO.write_to_database(Queries.INSERT_USER_QUIZ_SCORE, (score_id, user_id, score, timestamp))
    logger.debug('Score saved for: %s', username)

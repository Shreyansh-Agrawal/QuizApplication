'''Helper functions for Managing Quiz'''

import logging
from typing import Dict

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage, Prompts
from config.queries import Queries
from config.regex_patterns import RegexPattern
from controllers.category import CategoryController
from database.database_access import db
from models.quiz.question import Question
from models.quiz.option import Option
from utils import validations
from utils.custom_error import DataNotFoundError

logger = logging.getLogger(__name__)


class CreateQuizHelper:
    '''CreateQuizHelper class containing methods for managing quiz creation'''

    def get_question_data(self, username: str) -> Dict:
        '''Takes input of question details'''

        logger.debug(LogMessage.CREATE_ENTITY, Headers.QUES)
        print(DisplayMessage.CREATE_QUES_MSG)
        category_controller = CategoryController(db)
        user_choice = validations.regex_validator(
            prompt=Prompts.SELECT_CATEGORY_PROMPT,
            regex_pattern=RegexPattern.NUMERIC_PATTERN,
            error_msg=DisplayMessage.INVALID_CHOICE
        )
        user_choice = int(user_choice)
        categories = category_controller.get_all_categories()
        if user_choice > len(categories) or user_choice-1 < 0:
            raise DataNotFoundError(ErrorMessage.INVALID_CATEGORY_SELECTION_ERROR)

        category_name = categories[user_choice-1][0]
        category_id = db.read(Queries.GET_CATEGORY_ID_BY_NAME, (category_name, ))
        admin_data = db.read(Queries.GET_USER_ID_BY_USERNAME, (username, ))
        admin_id = admin_data[0][0]

        question_data = {}
        question_data['category_id'] = category_id[0][0]
        question_data['admin_id'] = admin_id
        question_data['admin_username'] = username
        question_data['question_text'] = validations.regex_validator(
            prompt=Prompts.QUES_TEXT_PROMPT,
            regex_pattern=RegexPattern.QUES_TEXT_PATTERN,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.QUES)
        ).title()

        return question_data

    def get_question_type(self, question_data: Dict) -> Dict:
        '''Get question type from user'''

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

        return question_data

    def create_option(self, question_data: Dict) -> Question:
        '''Create options, returns a question object'''

        question_data = self.get_question_type(question_data)
        question = Question.get_instance(question_data)

        match question_data['question_type']:
            case 'MCQ':
                option_data = {}
                option_data['question_id'] = question.entity_id
                option_data['option_text'] = validations.regex_validator(
                    prompt=Prompts.ANS_PROMPT,
                    regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                    error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
                ).title()
                option_data['is_correct'] = 1
                option = Option.get_instance(option_data)
                question.add_option(option)

                for _ in range(3):
                    option_data['question_id'] = question.entity_id
                    option_data['option_text'] = validations.regex_validator(
                        prompt=Prompts.OPTION_PROMPT,
                        regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
                    ).title()
                    option_data['is_correct'] = 0
                    option = Option.get_instance(option_data)
                    question.add_option(option)
            case 'T/F' | 'ONE WORD':
                option_data = {}
                option_data['question_id'] = question.entity_id
                option_data['option_text'] = validations.regex_validator(
                    prompt=Prompts.ANS_PROMPT,
                    regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                    error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
                ).title()
                option_data['is_correct'] = 1

                option = Option.get_instance(option_data)
                question.add_option(option)
            case _:
                logger.exception(LogMessage.INVALID_QUES_TYPE)
                return None

        return question

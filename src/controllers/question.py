'''Controllers for Operations related to Quiz'''

import logging
from ast import Dict
from typing import List, Tuple

import mysql.connector

from config.message_prompts import ErrorMessage, Headers, LogMessage
from config.queries import Queries
from controllers.user import UserController
from database.database_access import DatabaseAccess
from models.database.question_db import QuestionDB
from models.quiz.option import Option
from models.quiz.question import Question
from utils import validations
from utils.custom_error import DuplicateEntryError

logger = logging.getLogger(__name__)


class QuestionController:
    '''QuestionController class for quiz's question management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.question_db = QuestionDB(self.db)
        self.user_controller = UserController(self.db)

    def get_all_questions(self) -> List[Tuple]:
        '''Return all quiz questions'''

        data = self.db.read(Queries.GET_ALL_QUESTIONS_DETAIL)
        return data

    def get_random_questions(self) -> List[Tuple]:
        '''Return random questions across all categories'''

        data = self.db.read(Queries.GET_RANDOM_QUESTIONS)
        return data

    def get_questions_by_category(self, category_id: str) -> List[Tuple]:
        '''Return quiz questions by category'''

        logger.debug(LogMessage.GET_QUES_BY_CATEGORY)
        data = self.db.read(Queries.GET_QUESTIONS_BY_CATEGORY, (category_id, ))
        return data

    def get_random_questions_by_category(self, category: str) -> List[Tuple]:
        '''Return random questions by category'''

        data = self.db.read(Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY, (category, ))
        return data

    def create_question(self, category_id: str, question_data: Dict, admin_username: str) -> None:
        '''Add Questions in a Category'''

        data = self.user_controller.get_user_id(admin_username)
        admin_id = data[0].get('user_id')
        question_data['category_id'] = category_id
        question_data['admin_id'] = admin_id
        question_data['admin_username'] = admin_username

        question = Question.get_instance(question_data)

        option_data = {}
        option_data['question_id'] = question.entity_id
        option_data['option_text'] = question_data.get('answer')
        option_data['is_correct'] = 1
        option = Option.get_instance(option_data)
        question.add_option(option)

        for option in question_data.get('other_options'):
            option_data['question_id'] = question.entity_id
            option_data['option_text'] = option
            option_data['is_correct'] = 0
            option = Option.get_instance(option_data)
            question.add_option(option)
        try:
            self.question_db.save(question)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.QUES)) from e
        logger.debug(LogMessage.CREATE_SUCCESS, Headers.QUES)

    def post_quiz_data(self, quiz_data: Dict, admin_username: str) -> None:
        '''Posts quiz data to the database'''

        user_data = self.user_controller.get_user_id(admin_username)
        admin_id = user_data[0].get('user_id')
        for category_data in quiz_data['quiz_data']:
            category_id = validations.validate_id(entity='category')
            category_name = category_data['category']
            try:
                self.db.write(Queries.INSERT_CATEGORY, (category_id, admin_id, admin_username, category_name))
            except mysql.connector.IntegrityError as e:
                logger.debug(e)

            for question_data in category_data['question_data']:
                question_id = validations.validate_id(entity='question')
                question_text = question_data['question_text']
                question_type = question_data['question_type'].upper()
                answer_id = validations.validate_id(entity='option')
                answer_text = question_data['options']['answer']
                try:
                    self.db.write(
                        Queries.INSERT_QUESTION,
                        (question_id, category_id, admin_id, admin_username, question_text, question_type)
                    )
                    self.db.write(Queries.INSERT_OPTION, (answer_id, question_id, answer_text, 1))

                    if question_type.lower() == 'mcq':
                        for i in range(3):
                            other_option_id = validations.validate_id(entity='option')
                            other_option = question_data['options']['other_options'][i]

                            self.db.write(Queries.INSERT_OPTION, (other_option_id, question_id, other_option, 0))
                except mysql.connector.IntegrityError as e:
                    logger.debug(e)

    def update_question(self, question_id: str, new_ques_text: str) -> None:
        '''Update question text by question id'''
        try:
            self.db.write(Queries.UPDATE_QUESTION_TEXT_BY_ID, (new_ques_text, question_id))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.CATEGORY)) from e

    def delete_question(self, question_id: str) -> None:
        '''Delete a question and its options by question id'''

        self.db.write(Queries.DELETE_QUESTION_BY_ID, (question_id, ))

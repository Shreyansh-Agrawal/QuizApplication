'''Business logic for Operations related to Question'''

import logging
from typing import Dict, List

import mysql.connector

from config.queries import Queries
from config.string_constants import (
    ErrorMessage,
    Headers,
    LogMessage,
    QuestionTypes,
    StatusCodes
)
from database.database_access import DatabaseAccess
from models.quiz.option import Option
from models.quiz.question import Question
from utils.custom_error import DataNotFoundError, DuplicateEntryError
from utils.id_generator import generate_id

logger = logging.getLogger(__name__)


class QuestionBusiness:
    '''QuestionBusiness class for quiz's question management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database

    def get_quiz_data(self, category_id: str = None) -> List[Dict]:
        '''Return the quiz data in a specified category or across all categories'''

        logger.info(LogMessage.GET_QUIZ_DATA)

        query = Queries.GET_QUIZ_DATA
        params = ()
        if category_id:
            query += ' WHERE c.category_id = %s'
            params = (category_id, )

        query += ' ORDER BY c.category_id, q.question_id, o.option_id'
        data = self.db.read(query, params)
        if not data:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.QUIZ_NOT_FOUND)

        quiz_data = self.__format_quiz_data(data)
        return quiz_data

    def __format_quiz_data(self, data):
        '''Organize the data into the desired format'''

        quiz_data = []
        current_category = None
        current_question = None

        for question_data in data:
            if question_data['category_id'] != current_category:
                # New category
                current_category = question_data['category_id']
                quiz_data.append({
                    'category_id': current_category,
                    'category': question_data['category_name'],
                    'created_by': question_data['category_creator_id'],
                    'question_data': []
                })
                current_question = None

            if question_data['question_id'] != current_question:
                # New question
                current_question = question_data['question_id']
                correct_answer = None
                other_options = []

                if question_data['isCorrect']:
                    correct_answer = question_data['option_text']
                else:
                    other_options.append(question_data['option_text'])

                quiz_data[-1]['question_data'].append({
                    'question_id': current_question,
                    'question_text': question_data['question_text'],
                    'question_type': question_data['question_type'],
                    'created_by': question_data['question_creator_id'],
                    'options': {
                        'answer': correct_answer,
                        'other_options': other_options
                    }
                })
            else:
                # Additional option for the same question
                if question_data['isCorrect']:
                    correct_answer = question_data['option_text']
                else:
                    other_options.append(question_data['option_text'])

                quiz_data[-1]['question_data'][-1]['options'] = {
                    'answer': correct_answer,
                    'other_options': other_options
                }
        return quiz_data

    def create_question(self, category_id: str, question_data: Dict, admin_id: str) -> None:
        '''Add Questions in a Category'''

        logger.info(LogMessage.CREATE_ENTITY, Headers.QUES)

        question_data['category_id'] = category_id
        question_data['admin_id'] = admin_id
        question = Question.get_instance(question_data)

        option_data = {}
        option_data['question_id'] = question.entity_id
        option_data['option_text'] = question_data.get('answer')
        option_data['is_correct'] = 1
        option = Option.get_instance(option_data)
        question.add_option(option)

        # Organize the data into the desired format
        for option in question_data.get('other_options'):
            option_data['question_id'] = question.entity_id
            option_data['option_text'] = option
            option_data['is_correct'] = 0
            option = Option.get_instance(option_data)
            question.add_option(option)
        try:
            self.__save_question(question)
        except mysql.connector.IntegrityError as e:
            logger.exception(e)
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.QUESTION_EXISTS) from e

        logger.info(LogMessage.CREATE_SUCCESS, Headers.QUES)

    def __save_question(self, entity: Question) -> None:
        '''Adds the question to the database.'''

        question_data = (
            entity.entity_id,
            entity.category_id,
            entity.admin_id,
            entity.text,
            entity.question_type
        )
        if not entity.options:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.NO_OPTIONS)

        self.db.write(Queries.INSERT_QUESTION, question_data)
        for option in entity.options:
            self.__save_option(option)

    def __save_option(self, entity: Option) -> None:
        '''Adds the option to the database.'''

        option_data = (
            entity.entity_id,
            entity.question_id,
            entity.text,
            entity.is_correct
        )
        self.db.write(Queries.INSERT_OPTION, option_data)

    def post_quiz_data(self, quiz_data: Dict, admin_id: str) -> None:
        '''Posts quiz data to the database'''

        logger.info(LogMessage.POST_QUIZ_DATA)

        # Organize the data into the desired format
        for category_data in quiz_data['quiz_data']:
            category_id = generate_id(entity='category')
            category_name = category_data['category']
            try:
                self.db.write(Queries.INSERT_CATEGORY, (category_id, admin_id, category_name))
            except mysql.connector.IntegrityError as e:
                logger.info(e)

            for question_data in category_data['question_data']:
                question_id = generate_id(entity='question')
                question_text = question_data['question_text']
                question_type = question_data['question_type']
                answer_id = generate_id(entity='option')
                answer_text = question_data['options']['answer']
                try:
                    self.db.write(
                        Queries.INSERT_QUESTION,
                        (question_id, category_id, admin_id, question_text, question_type)
                    )
                    self.db.write(Queries.INSERT_OPTION, (answer_id, question_id, answer_text, 1))

                    if question_type.lower() == QuestionTypes.MCQ:
                        for i in range(3):
                            other_option_id = generate_id(entity='option')
                            other_option = question_data['options']['other_options'][i]

                            self.db.write(Queries.INSERT_OPTION, (other_option_id, question_id, other_option, 0))
                except mysql.connector.IntegrityError as e:
                    logger.info(e)

    def update_question(self, question_id: str, new_ques_text: str) -> None:
        '''Update question text by question id'''

        logger.info(LogMessage.UPDATE_ENTITY, Headers.QUES)

        try:
            row_affected = self.db.write(Queries.UPDATE_QUESTION_TEXT_BY_ID, (new_ques_text, question_id))
        except mysql.connector.IntegrityError as e:
            logger.exception(e)
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.QUESTION_EXISTS) from e
        if not row_affected:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.QUESTION_NOT_FOUND)

        logger.info(LogMessage.UPDATE_SUCCESS, Headers.QUES)

    def delete_question(self, question_id: str) -> None:
        '''Delete a question and its options by question id'''

        logger.warning(LogMessage.DELETE_ENTITY, Headers.QUES)

        row_affected = self.db.write(Queries.DELETE_QUESTION_BY_ID, (question_id, ))
        if not row_affected:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.QUESTION_NOT_FOUND)

        logger.info(LogMessage.DELETE_SUCCESS, Headers.QUES)

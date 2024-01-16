'''Controllers for Operations related to Quiz'''

import logging
from typing import List, Tuple

import mysql.connector

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage
from config.queries import Queries
from helpers.create_quiz_helper import CreateQuizHelper
from models.quiz.question import QuestionDB
from utils.custom_error import DuplicateEntryError

logger = logging.getLogger(__name__)


class QuestionController:
    '''QuestionController class for quiz's question management'''

    def __init__(self, database) -> None:
        self.db = database

    def get_all_questions(self) -> List[Tuple]:
        '''Return all quiz questions'''

        data = self.db.read(Queries.GET_ALL_QUESTIONS_DETAIL)
        return data

    def get_random_questions(self) -> List[Tuple]:
        '''Return random questions across all categories'''

        data = self.db.read(Queries.GET_RANDOM_QUESTIONS)
        return data

    def get_questions_by_category(self, category_name: str) -> List[Tuple]:
        '''Return quiz questions by category'''

        logger.debug(LogMessage.GET_QUES_BY_CATEGORY)
        data = self.db.read(Queries.GET_QUESTIONS_BY_CATEGORY, (category_name, ))
        return data

    def get_random_questions_by_category(self, category: str) -> List[Tuple]:
        '''Return random questions by category'''

        data = self.db.read(Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY, (category, ))
        return data

    def create_question(self, username: str) -> None:
        '''Add Questions in a Category'''

        create_quiz_helper = CreateQuizHelper()
        question_data = create_quiz_helper.get_question_data(username)
        question = create_quiz_helper.create_option(question_data)

        try:
            QuestionDB.save(question)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.QUES)) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.QUES)
        print(DisplayMessage.CREATE_QUES_SUCCESS_MSG)

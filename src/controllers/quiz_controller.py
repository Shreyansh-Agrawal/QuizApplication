'''Controllers for Operations related to Quiz'''

import logging
import mysql.connector
import time
from typing import Dict, List, Tuple

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage
from config.queries import Queries
from controllers.helpers.create_quiz_helper import CreateQuizHelper
from controllers.helpers.start_quiz_helper import StartQuizHelper
from database.database_access import db
from models.quiz import Category
from utils.custom_error import DataNotFoundError, DuplicateEntryError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


class QuizController:
    '''QuizController class containing methods related to managing quiz'''

    def get_all_questions(self) -> List[Tuple]:
        '''Return all quiz questions'''

        data = db.read_from_database(Queries.GET_ALL_QUESTIONS_DETAIL)
        return data

    def get_questions_by_category(self, category_name: str) -> List[Tuple]:
        '''Return quiz questions by category'''

        logger.debug(LogMessage.GET_QUES_BY_CATEGORY)
        data = db.read_from_database(Queries.GET_QUESTIONS_BY_CATEGORY, (category_name, ))
        return data

    def get_leaderboard(self) -> List[Tuple]:
        '''Return top 10 scores for leaderboard'''

        data = db.read_from_database(Queries.GET_LEADERBOARD)
        return data

    def create_category(self, category_data: Dict) -> None:
        '''Add a Quiz Category'''

        logger.debug(LogMessage.CREATE_ENTITY, Headers.CATEGORY)
        category = Category(category_data)

        try:
            category.save_to_database()
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.CATEGORY)) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.CATEGORY)
        print(DisplayMessage.CREATE_CATEGORY_SUCCESS_MSG)

    def create_question(self, username: str) -> None:
        '''Add Questions in a Category'''

        create_quiz_helper = CreateQuizHelper()
        question_data = create_quiz_helper.get_question_data(username)
        question = create_quiz_helper.create_option(question_data)

        try:
            question.save_to_database()
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.QUES)) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.QUES)
        print(DisplayMessage.CREATE_QUES_SUCCESS_MSG)

    def update_category_by_name(self, old_category_name: str, new_category_name: str) -> None:
        '''Update a category by category name'''

        logger.debug(LogMessage.UPDATE_ENTITY, Headers.CATEGORY)
        try:
            db.write_to_database(Queries.UPDATE_CATEGORY_BY_NAME, (new_category_name, old_category_name))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.CATEGORY)) from e

        logger.debug(LogMessage.UPDATE_CATEGORY_SUCCESS, old_category_name, new_category_name)
        print(
            DisplayMessage.UPDATE_CATEGORY_SUCCESS_MSG.format(
                name=old_category_name, new_name=new_category_name
            )
        )

    def delete_category_by_name(self, category_name: str) -> None:
        '''Delete a category by category name'''

        logger.warning(LogMessage.DELETE_CATEGORY, category_name)
        db.write_to_database(Queries.DELETE_CATEGORY_BY_NAME, (category_name, ))

        logger.debug(LogMessage.DELETE_CATEGORY_SUCCESS, category_name)
        print(DisplayMessage.DELETE_CATEGORY_SUCCESS_MSG.format(name=category_name))

    def start_quiz(self, username: str, category: str = None) -> None:
        '''Start a New Quiz'''

        logger.debug(LogMessage.START_QUIZ, username)
        start_quiz_helper = StartQuizHelper()
        if not category:
            data = start_quiz_helper.get_random_questions()
        else:
            data = start_quiz_helper.get_random_questions_by_category(category)
        if len(data) < 10:
            raise DataNotFoundError(ErrorMessage.INSUFFICIENT_QUESTIONS_ERROR)

        print(DisplayMessage.QUIZ_START_MSG)
        end_time = time.time() + 5*60
        score = 0
        player_responses = []

        # Display question, take player's response and calculate score one by one
        for question_no, question_data in enumerate(data, 1):
            question_id, question_text, question_type, correct_answer = question_data
            options_data = db.read_from_database(Queries.GET_OPTIONS_FOR_MCQ, (question_id, ))

            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                print('\nTime\'s up!') # pragma: no cover
                break # pragma: no cover

            mins = int(remaining_time // 60)
            formatted_mins = str(mins).zfill(2)
            seconds = int(remaining_time % 60)
            formatted_seconds = str(seconds).zfill(2)
            print(f'\nTime remaining: {formatted_mins}:{formatted_seconds} mins')

            start_quiz_helper.display_question(question_no, question_text, question_type, options_data)
            player_answer = start_quiz_helper.get_player_response(question_type)

            if question_type.lower() == 'mcq':
                player_answer = options_data[player_answer-1][0]
            if player_answer.lower() == correct_answer.lower():
                score += 10
            player_responses.append((question_text, player_answer, correct_answer))

        print(DisplayMessage.DISPLAY_SCORE_MSG.format(score=score))
        print(DisplayMessage.REVIEW_RESPONSES_MSG)
        pretty_print(data=player_responses, headers=(Headers.QUES, Headers.PLAYER_ANS, Headers.ANS))
        start_quiz_helper.save_quiz_score(username, score)
        logger.debug(LogMessage.COMPLETE_QUIZ, username)

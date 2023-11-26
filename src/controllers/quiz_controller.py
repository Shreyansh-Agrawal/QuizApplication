'''Controllers for Operations related to Quiz'''

import logging
import sqlite3
import time
from typing import Dict, List, Tuple

from config.message_prompts import DisplayMessage, Headers, LogMessage
from config.queries import Queries
from controllers.helpers import quiz_helper as QuizHelper
from controllers.helpers import start_quiz_helper as StartQuizHelper
from database.database_access import DatabaseAccess as DAO
from models.quiz import Category
from utils.custom_error import DataNotFoundError, DuplicateEntryError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


class QuizController:
    '''QuizController class containing methods related to managing quiz'''

    def get_all_questions(self) -> List[Tuple]:
        '''Return all quiz questions'''

        data = DAO.read_from_database(Queries.GET_ALL_QUESTIONS_DETAIL)
        return data

    def get_questions_by_category(self, category_name: str) -> List[Tuple]:
        '''Return quiz questions by category'''

        logger.debug(LogMessage.GET_QUES_BY_CATEGORY)
        data = DAO.read_from_database(Queries.GET_QUESTIONS_BY_CATEGORY, (category_name, ))
        return data

    def get_leaderboard(self) -> List[Tuple]:
        '''Return top 10 scores for leaderboard'''

        data = DAO.read_from_database(Queries.GET_LEADERBOARD)
        return data

    def create_category(self, category_data: Dict) -> None:
        '''Add a Quiz Category'''

        logger.debug(LogMessage.CREATE_ENTITY, Headers.CATEGORY)
        category = Category(category_data)

        try:
            category.save_to_database()
        except sqlite3.IntegrityError as e:
            raise DuplicateEntryError('Category already exists!') from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.CATEGORY)
        print(DisplayMessage.CREATE_CATEGORY_SUCCESS_MSG)

    def create_question(self, username: str) -> None:
        '''Add Questions in a Category'''

        question_data = QuizHelper.get_question_data(username)
        question = QuizHelper.create_option(question_data)

        try:
            question.save_to_database()
        except sqlite3.IntegrityError as e:
            raise DuplicateEntryError('Question already exists!') from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.QUES)
        print(DisplayMessage.CREATE_QUES_SUCCESS_MSG)

    def update_category_by_name(self, old_category_name: str, new_category_name: str) -> None:
        '''Update a category by category name'''

        logger.debug(LogMessage.UPDATE_ENTITY, Headers.CATEGORY)
        try:
            DAO.write_to_database(Queries.UPDATE_CATEGORY_BY_NAME, (new_category_name, old_category_name))
        except sqlite3.IntegrityError as e:
            raise DuplicateEntryError('Category already exists!') from e

        logger.debug(LogMessage.UPDATE_CATEGORY_SUCCESS, old_category_name, new_category_name)
        print(DisplayMessage.UPDATE_CATEGORY_SUCCESS_MSG.format(name=old_category_name, new_name=new_category_name))

    def delete_category_by_name(self, category_name: str) -> None:
        '''Delete a category by category name'''

        logger.warning(LogMessage.DELETE_CATEGORY, category_name)
        DAO.write_to_database(Queries.DELETE_CATEGORY_BY_NAME, (category_name, ))

        logger.debug(LogMessage.DELETE_CATEGORY_SUCCESS, category_name)
        print(DisplayMessage.DELETE_CATEGORY_SUCCESS_MSG.format(name=category_name))

    def start_quiz(self, username: str, category: str = None) -> None:
        '''Start a New Quiz'''

        logger.debug(LogMessage.START_QUIZ, username)
        if not category:
            data = StartQuizHelper.get_random_questions()
        else:
            data = StartQuizHelper.get_random_questions_by_category(category)

        if len(data) < 10:
            raise DataNotFoundError('Not enough questions!')

        print(DisplayMessage.QUIZ_START_MSG)
        end_time = time.time() + 5*60
        score = 0
        player_responses = []

        # Display question, take player's response and calculate score one by one
        for question_no, question_data in enumerate(data, 1):
            question_id, question_text, question_type, correct_answer = question_data
            options_data = DAO.read_from_database(Queries.GET_OPTIONS_FOR_MCQ, (question_id, ))

            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                print('\nTime\'s up!')
                break

            mins = int(remaining_time // 60)
            formatted_mins = str(mins).zfill(2)
            seconds = int(remaining_time % 60)
            formatted_seconds = str(seconds).zfill(2)
            print(f'\nTime remaining: {formatted_mins}:{formatted_seconds} mins')

            StartQuizHelper.display_question(question_no, question_text, question_type, options_data)

            player_answer = StartQuizHelper.get_player_response(question_type)

            if question_type.lower() == 'mcq':
                player_answer = options_data[player_answer-1][0]

            if player_answer.lower() == correct_answer.lower():
                score += 10

            player_responses.append((question_text, player_answer, correct_answer))

        print(DisplayMessage.DISPLAY_SCORE_MSG.format(score=score))
        print('\n-----REVIEW YOUR RESPONSES-----\n')
        pretty_print(data=player_responses, headers=(Headers.QUES, Headers.PLAYER_ANS, Headers.ANS))
        StartQuizHelper.save_quiz_score(username, score)
        logger.debug(LogMessage.COMPLETE_QUIZ, username)

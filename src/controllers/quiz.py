'''Controllers for Operations related to Quiz'''

import logging
import time
from typing import List, Tuple

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage
from config.queries import Queries
from helpers.start_quiz_helper import StartQuizHelper
from controllers.question import QuestionController
from database.database_access import DatabaseAccess
from utils.custom_error import DataNotFoundError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


class QuizController:
    '''QuizController class for quiz management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database

    def get_leaderboard(self) -> List[Tuple]:
        '''Return top 10 scores for leaderboard'''

        data = self.db.read(Queries.GET_LEADERBOARD)
        return data

    def start_quiz(self, username: str, category: str = None) -> None:
        '''Start a New Quiz'''

        logger.debug(LogMessage.START_QUIZ, username)
        db = DatabaseAccess()
        question_controller = QuestionController(db)
        start_quiz_helper = StartQuizHelper()
        if not category:
            data = question_controller.get_random_questions()
        else:
            data = question_controller.get_random_questions_by_category(category)
        if len(data) < 10:
            raise DataNotFoundError(ErrorMessage.INSUFFICIENT_QUESTIONS_ERROR)

        print(DisplayMessage.QUIZ_START_MSG)
        end_time = time.time() + 5*60
        score = 0
        player_responses = []

        # Display question, take player's response and calculate score one by one
        for question_no, question_data in enumerate(data, 1):
            question_id, question_text, question_type, correct_answer = question_data
            options_data = self.db.read(Queries.GET_OPTIONS_FOR_MCQ, (question_id, ))

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

'''Controllers for Operations related to Quiz'''

import logging
from typing import Dict, List

from business.quiz_business import QuizBusiness
from config.message_prompts import Message, StatusCodes
from database.database_access import DatabaseAccess
from utils.custom_response import SuccessMessage
from utils.error_handlers import handle_custom_errors

logger = logging.getLogger(__name__)


class QuizController:
    '''QuizController class for quiz management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.quiz_business = QuizBusiness(self.db)

    @handle_custom_errors
    def get_leaderboard(self):
        '''Return top 10 scores for leaderboard'''

        leaderboard_data = self.quiz_business.get_leaderboard()
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=leaderboard_data).message_info

    @handle_custom_errors
    def get_player_scores(self, player_id: str):
        '''Return user's scores'''

        scores = self.quiz_business.get_player_scores(player_id)
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=scores).message_info

    @handle_custom_errors
    def get_random_questions(self, category_id: str = None, question_type: str = None, limit: int = 10):
        '''
        Return random questions for quiz
        Filters: category_id, question_type, limit
        '''

        question_data = self.quiz_business.get_random_questions(category_id, question_type, limit)
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=question_data).message_info

    @handle_custom_errors
    def evaluate_player_answers(self, player_id: str, player_answers: List[Dict]):
        'Evaluate player answers and return score with correct answers'

        result = self.quiz_business.evaluate_player_answers(player_id, player_answers)
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.SUBMISSION_SUCCESS, data=result).message_info

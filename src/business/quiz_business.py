'''Business logic for Operations related to Quiz'''

import logging
from datetime import datetime, timezone
from typing import Dict, List

from config.queries import Queries
from config.string_constants import ErrorMessage, LogMessage, StatusCodes, QuestionTypes
from database.database_access import DatabaseAccess
from utils.custom_error import DataNotFoundError
from utils.id_generator import generate_id

logger = logging.getLogger(__name__)


class QuizBusiness:
    '''QuizBusiness class for quiz management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database

    def get_leaderboard(self) -> List[Dict]:
        '''Return top 10 scores for leaderboard'''

        logger.info(LogMessage.GET_LEADERBOARD)

        data = self.db.read(Queries.GET_LEADERBOARD)
        if not data:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.LEADERBOARD_NOT_FOUND)
        return data

    def get_player_scores(self, player_id: str) -> List[Dict]:
        '''Return user's scores'''

        logger.info(LogMessage.GET_SCORES, player_id)

        data = self.db.read(Queries.GET_PLAYER_SCORES_BY_ID, (player_id, ))
        if not data:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.SCORES_NOT_FOUND)
        return data

    def get_random_questions(self, category_id: str = None, question_type: str = None, limit: int = 10) -> List[Dict]:
        '''
        Return random questions for quiz
        Filters: category_id, question_type, limit
        '''

        logger.info(LogMessage.GET_QUES_FOR_QUIZ)

        question_data = self.db.read(
            Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY, (category_id, category_id, question_type, question_type, limit)
        )
        if len(question_data) < limit:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.QUESTIONS_NOT_FOUND)

        # Organize the data into the desired format
        result = [
            {
                'question_id': question['question_id'],
                'question_text': question['question_text'],
                'question_type': question['question_type'],
                'options': question['options'].split(',') if question['question_type'].lower() == QuestionTypes.MCQ else []
            }
            for question in question_data
        ]
        return result

    def evaluate_player_answers(self, player_id: str, player_answers: List[Dict]) -> Dict:
        'Evaluate player answers and return score with correct answers'

        logger.info(LogMessage.EVALUATE_RESPONSE, player_id)

        question_ids = tuple(response['question_id'] for response in player_answers)
        no_of_questions = len(question_ids)
        formatted_query = Queries.GET_QUESTION_DATA_BY_QUESTION_ID % (', '.join(['%s'] * no_of_questions))
        question_data = self.db.read(formatted_query, question_ids)

        question_data = sorted(question_data, key=lambda x: x['question_id'])
        player_answers = sorted(player_answers, key=lambda x: x['question_id'])

        result = self.__format_result(question_data, player_answers)
        normalized_score = self.__normalize_score(result['score'], no_of_questions)
        result['score'] = normalized_score

        self.__save_quiz_score(player_id, normalized_score)
        return result

    def __format_result(self, question_data, player_answers):
        'Organize the result into the desired format'

        result = {
            'score': 0,
            'responses': []
        }
        for question_data, player_answers in zip(question_data, player_answers):
            correct_answer = question_data['correct_answer']
            is_correct = player_answers['user_answer'].lower() == correct_answer.lower()
            result['responses'].append({
                'question_id': question_data['question_id'],
                'question_text': question_data['question_text'],
                'user_answer': player_answers['user_answer'],
                'correct_answer': correct_answer,
                'is_correct': is_correct
            })
            if is_correct:
                result['score'] += 1

        return result

    def __normalize_score(self, score: int, no_of_questions):
        'Normalize the score obtained on a scale of [0, 100]'

        normalized_score = (score/no_of_questions) * 100
        return normalized_score

    def __save_quiz_score(self, player_id: str, score: int) -> None:
        '''Save Player's Quiz Score'''

        logger.info(LogMessage.SAVE_QUIZ_SCORE, player_id)

        score_id = generate_id(entity='score')
        time = datetime.now(timezone.utc) # current utc time
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

        self.db.write(Queries.INSERT_PLAYER_QUIZ_SCORE, (score_id, player_id, score, timestamp))
        logger.info(LogMessage.SAVE_QUIZ_SCORE_SUCCESS, player_id)

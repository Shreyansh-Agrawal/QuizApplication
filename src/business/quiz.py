'''Business logic for Operations related to Quiz'''

import logging
from datetime import datetime, timezone
from typing import Dict, List

from config.message_prompts import ErrorMessage, StatusCodes
from config.queries import Queries
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

        data = self.db.read(Queries.GET_LEADERBOARD)
        if not data:
            raise DataNotFoundError(StatusCodes.NOT_FOUND, message=ErrorMessage.LEADERBOARD_NOT_FOUND)
        return data

    def get_player_scores(self, player_id: str) -> List[Dict]:
        '''Return user's scores'''

        data = self.db.read(Queries.GET_PLAYER_SCORES_BY_ID, (player_id, ))
        if not data:
            raise DataNotFoundError(StatusCodes.NOT_FOUND, message=ErrorMessage.SCORES_NOT_FOUND)
        return data

    def get_random_questions(self, category_id: str = None) -> List[Dict]:
        '''Return random questions in a category if category_id present else across all categories'''

        query = Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY if category_id else Queries.GET_RANDOM_QUESTIONS
        question_data = self.db.read(query, (category_id, ) if category_id else ())
        if len(question_data) < 10:
            raise DataNotFoundError(StatusCodes.NOT_FOUND, message=ErrorMessage.QUESTIONS_NOT_FOUND)

        # Organize the data into the desired format
        result = [
            {
                'question_id': question['question_id'],
                'question_text': question['question_text'],
                'question_type': question['question_type'],
                'options': question['options'].split(',') if question['question_type'].lower() == 'mcq' else []
            }
            for question in question_data
        ]
        return result

    def save_quiz_score(self, player_id: str, score: int) -> None:
        '''Save Player's Quiz Score'''

        score_id = generate_id(entity='score')
        time = datetime.now(timezone.utc) # current utc time
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

        self.db.write(Queries.INSERT_PLAYER_QUIZ_SCORE, (score_id, player_id, score, timestamp))

    def evaluate_player_answers(self, player_id: str, player_answers: List[Dict]) -> Dict:
        'Evaluate player answers and return score with correct answers'

        question_ids = tuple(response['question_id'] for response in player_answers)
        formatted_query = Queries.GET_QUESTION_DATA_BY_QUESTION_ID % (', '.join(['%s'] * len(question_ids)))
        question_data = self.db.read(formatted_query, question_ids)
        result = {
            'score': 0,
            'responses': []
        }
        question_data = sorted(question_data, key=lambda x: x['question_id'])
        player_answers = sorted(player_answers, key=lambda x: x['question_id'])

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
                result['score'] += 10

        self.save_quiz_score(player_id, result['score'])
        return result

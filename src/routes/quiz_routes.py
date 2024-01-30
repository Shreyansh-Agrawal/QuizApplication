'Routes for the Quiz related functionalities'

from typing import Annotated, List

from fastapi import APIRouter, Depends, Response

from config.message_prompts import Roles
from controllers.quiz_controller import QuizController
from database.database_access import DatabaseAccess
from schemas.quiz import AnswerSchema
from utils.rbac import access_level
from utils.token_handler import get_jwt

router = APIRouter(tags=['Quiz'])

db = DatabaseAccess()
quiz_controller = QuizController(db)
user_dependency = Annotated[dict, Depends(get_jwt)]


@router.get('/leaderboard')
@access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
def get_leaderboard(claims: user_dependency, response: Response):
    'Get leaderboard details'
    res = quiz_controller.get_leaderboard()
    response.status_code = res.status.code
    return res.message_info


@router.get('/scores/me')
@access_level(roles=[Roles.PLAYER])
def get_player_scores(claims: user_dependency, response: Response):
    'Get past scores of a player'
    user_id = claims.get('sub')
    res = quiz_controller.get_player_scores(user_id)
    response.status_code = res.status.code
    return res.message_info


@router.get('/quiz')
@access_level(roles=[Roles.PLAYER])
def get_random_questions(claims: user_dependency, response: Response, category_id: str | None = None):
    '''
    Get random questions for quiz
    Query Parameters: category_id
    '''
    res = quiz_controller.get_random_questions(category_id)
    response.status_code = res.status.code
    return res.message_info


@router.post('/quiz/answers')
@access_level(roles=[Roles.PLAYER])
def evaluate_player_answers(claims: user_dependency, player_answers: List[AnswerSchema], response: Response):
    'Post player responses to the questions'
    user_id = claims.get('sub')
    res = quiz_controller.evaluate_player_answers(user_id, player_answers)
    response.status_code = res.status.code
    return res.message_info

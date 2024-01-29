'Routes for the Question related functionalities'

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from config.message_prompts import Roles
from controllers.question_controller import QuestionController
from controllers.user_controller import UserController
from database.database_access import DatabaseAccess
from schemas.question import QuestionSchema, QuizDataSchema, QuestionUpdateSchema
from utils.rbac import access_level
from utils.token_handler import get_jwt

router = APIRouter(tags=['Question'])

db = DatabaseAccess()
question_controller = QuestionController(db)
user_controller = UserController(db)
user_dependency = Annotated[dict, Depends(get_jwt)]


@router.get('/categories/questions')
@access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
def get_quiz_data(claims: user_dependency, response: Response, category_id: str | None = None):
    '''
    Get quiz data in a specified category or across all categories
    Query Parameters: category_id
    '''
    res = question_controller.get_quiz_data(category_id)
    response.status_code = res.status.code
    return res.message_info


@router.post('/categories/questions')
@access_level(roles=[Roles.ADMIN])
def post_quiz_data(claims: user_dependency, quiz_data: QuizDataSchema, response: Response):
    'Upload quiz data including questions, categories and options'
    user_id = claims.get('sub')
    res = question_controller.post_quiz_data(dict(quiz_data), user_id)
    response.status_code = res.status.code
    return res.message_info


@router.post('/categories/{category_id}/questions')
@access_level(roles=[Roles.ADMIN])
def create_question(claims: user_dependency, question_data: QuestionSchema, category_id: str, response: Response):
    'Create a question in a specified category'
    user_id = claims.get('sub')
    res = question_controller.create_question(category_id, dict(question_data), user_id)
    response.status_code = res.status.code
    return res.message_info


@router.patch('/categories/questions/{question_id}')
@access_level(roles=[Roles.ADMIN])
def update_question(claims: user_dependency, question_data: QuestionUpdateSchema, question_id: str, response: Response):
    'Update a question text'
    res = question_controller.update_question(question_id, dict(question_data))
    response.status_code = res.status.code
    return res.message_info


@router.delete('/categories/questions/{question_id}')
@access_level(roles=[Roles.ADMIN])
def delete_question(claims: user_dependency, question_id: str, response: Response):
    'Delete a question and its options'
    res = question_controller.delete_question(question_id)
    response.status_code = res.status.code
    return res.message_info

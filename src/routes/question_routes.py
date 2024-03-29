'Routes for the Question related functionalities'

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from config.string_constants import AUTHORIZATION_HEADER, Roles
from controllers.question_controller import QuestionController
from controllers.user_controller import UserController
from database.database_access import DatabaseAccess
from schemas.config_schema import ResponseSchema
from schemas.question import (
    QuestionParamSchema,
    QuestionSchema,
    QuestionUpdateSchema,
    QuizDataSchema,
    QuizResponseSchema
)
from utils.rbac import access_level

blp = Blueprint('Question', __name__, description='Routes for the Question related functionalities')

db = DatabaseAccess()
question_controller = QuestionController(db)
user_controller = UserController(db)


@blp.route('/categories/questions')
class Question(MethodView):
    '''
    Routes to:
        Get quiz data in a specified category or across all categories
        Post quiz data including questions, categories and options
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    @blp.arguments(QuestionParamSchema, location='query')
    @blp.response(200, QuizResponseSchema)
    @blp.doc(parameters=[AUTHORIZATION_HEADER])

    def get(self, query_params):
        '''
        Get quiz data in a specified category or across all categories
        Query Parameters: category_id
        '''
        return question_controller.get_quiz_data(**query_params)

    @access_level(roles=[Roles.ADMIN])
    @blp.arguments(QuizDataSchema)
    @blp.response(201, ResponseSchema)
    @blp.doc(parameters=[AUTHORIZATION_HEADER])

    def post(self, quiz_data):
        'Post quiz data including questions, categories and options'
        admin_id= get_jwt_identity()
        return question_controller.post_quiz_data(quiz_data, admin_id)


@blp.route('/categories/<string:category_id>/questions')
class QuestionByCategoryId(MethodView):
    '''
    Routes to:
        Create a question in a specified category
    '''

    @access_level(roles=[Roles.ADMIN])
    @blp.arguments(QuestionSchema)
    @blp.response(201, ResponseSchema)
    @blp.doc(parameters=[AUTHORIZATION_HEADER])

    def post(self, question_data, category_id):
        'Create a question in a specified category'
        admin_id = get_jwt_identity()
        return question_controller.create_question(category_id, question_data, admin_id)


@blp.route('/categories/questions/<string:question_id>')
class QuestionById(MethodView):
    '''
    Routes to:
        Update a question text
        Delete a question and its options
    '''

    @access_level(roles=[Roles.ADMIN])
    @blp.arguments(QuestionUpdateSchema)
    @blp.response(200, ResponseSchema)
    @blp.doc(parameters=[AUTHORIZATION_HEADER])

    def put(self, question_data, question_id):
        'Update a question text'
        return question_controller.update_question(question_id, question_data)

    @access_level(roles=[Roles.ADMIN], check_fresh=True)
    @blp.response(200, ResponseSchema)
    @blp.doc(parameters=[AUTHORIZATION_HEADER])

    def delete(self, question_id):
        'Delete a question and its options'
        return question_controller.delete_question(question_id)

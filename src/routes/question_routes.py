'Routes for the Question related functionalities'

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from config.message_prompts import Roles
from controllers.question_controller import QuestionController
from controllers.user_controller import UserController
from database.database_access import DatabaseAccess
from schemas.question import QuestionSchema, QuizDataSchema, QuestionUpdateSchema
from utils.rbac import access_level

blp = Blueprint('Question', __name__, description='Routes for the Question related functionalities')

db = DatabaseAccess()
question_controller = QuestionController(db)
user_controller = UserController(db)


@blp.route('/categories/questions')
class Question(MethodView):
    '''
    Routes to:
        Get all questions in a specified category or across all categories
        Post quiz data including questions, categories and options
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def get(self):
        '''
        Get quiz data in a specified category or across all categories
        Query Parameters: category_id
        '''
        category_id = request.args.get('category_id')
        return question_controller.get_quiz_data(category_id)

    @access_level(roles=[Roles.ADMIN])
    @blp.arguments(QuizDataSchema)
    def post(self, quiz_data):
        'Upload quiz data including questions, categories and options'
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
    def patch(self, question_data, question_id):
        'Update a question text'
        return question_controller.update_question(question_id, question_data)

    @access_level(roles=[Roles.ADMIN])
    def delete(self, question_id):
        'Delete a question and its options'
        return question_controller.delete_question(question_id)

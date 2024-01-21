'Routes for the Question related functionalities'

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint, abort

from config.message_prompts import Roles
from controllers.question import QuestionController
from controllers.user import UserController
from database.database_access import DatabaseAccess
from schemas.question import QuestionSchema, QuizDataSchema, QuestionUpdateSchema
from utils.custom_error import DuplicateEntryError
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
    # @blp.response(200, QuestionSchema(many=True))
    def get(self):
        '''
        Get quiz data in a specified category or across all categories

        Query Parameters: category_id
        '''
        category_id = request.args.get('category_id')
        quiz_data = question_controller.get_quiz_data(category_id)

        if not quiz_data:
            abort(404, message='No questions present')
        return {'quiz_data': quiz_data}

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    @blp.arguments(QuizDataSchema)
    def post(self, quiz_data):
        'Upload quiz data including questions, categories and options'

        admin_username = get_jwt_identity()
        question_controller.post_quiz_data(quiz_data, admin_username)

        return {'message': 'Posted Quiz data successfully'}, 201


@blp.route('/categories/<string:category_id>/questions')
class QuestionByCategoryId(MethodView):
    '''
    Routes to:
        Create a question in a specified category
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    @blp.arguments(QuestionSchema)
    def post(self, question_data, category_id):
        'Create a question in a specified category'

        admin_username = get_jwt_identity()
        try:
            question_controller.create_question(category_id, question_data, admin_username)
        except DuplicateEntryError as e:
            abort(409, message=str(e))

        return {'message': 'Question added successfully'}, 201


@blp.route('/categories/questions/<string:question_id>')
class QuestionById(MethodView):
    '''
    Routes to:
        Update a question text
        Delete a question and its options
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    @blp.arguments(QuestionUpdateSchema)
    def patch(self, question_data, question_id):
        'Update a question text'

        new_ques_text = question_data.get('question_text')
        try:
            question_controller.update_question(question_id, new_ques_text)
        except DuplicateEntryError as e:
            abort(409, message=str(e))

        return {'message': "Question updated successfully"}

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def delete(self, question_id):
        'Delete a question and its options'

        question_controller.delete_question(question_id)
        return {'message': "Question deleted successfully"}

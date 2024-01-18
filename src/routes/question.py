'Routes for the Question related functionalities'

from flask.views import MethodView
from flask_smorest import Blueprint

from config.message_prompts import Roles
from utils.rbac import access_level

blp = Blueprint('Question', __name__)


@blp.route('/categories/questions')
class Question(MethodView):
    '''
    Routes to:
        Get all questions across all categories
        Get all questions in a specified category
        Post quiz data including questions, categories and options
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def get(self):
        '''
        Get all questions in a specified category or across all categories

        Query Parameters: category_id
        '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def post(self):
        'Upload quiz data including questions, categories and options'


@blp.route('/categories/<string:category_id>/questions')
class QuestionByCategoryId(MethodView):
    '''
    Routes to:
        Create a question in a specified category
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def post(self, category_id):
        'Create a question in a specified category'


@blp.route('/categories/questions/<string:question_id>')
class QuestionById(MethodView):
    '''
    Routes to:
        Update a question text
        Delete a question and its options
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def patch(self):
        'Update a question text'

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def delete(self):
        'Delete a question and its options'

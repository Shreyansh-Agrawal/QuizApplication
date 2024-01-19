'Routes for the Category related functionalities'

from flask.views import MethodView
from flask_smorest import Blueprint

from config.message_prompts import Roles
from utils.rbac import access_level

blp = Blueprint('Category', __name__, description='Routes for the Category related functionalities')


@blp.route('/categories')
class Category(MethodView):
    '''
    Routes to:
        Get all categories details
        Create a new category
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    def get(self):
        'Get all categories details'

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def post(self):
        'Create a new category'


@blp.route('/categories/<string:category_id>')
class CategoryById(MethodView):
    '''
    Routes to:
        Update an existing category
        Delete an existing category
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def put(self, category_id):
        'Update an existing category'

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def delete(self, category_id):
        'Delete an existing category'

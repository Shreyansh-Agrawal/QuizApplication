'Routes for the Category related functionalities'

from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint('Category', __name__)


@blp.route('/categories')
class Category(MethodView):
    '''
    Routes to:
        Get all categories details
        Create a new category
    '''

    def get(self):
        'Get all categories details'

    def post(self):
        'Create a new category'


@blp.route('/categories/<string:category_id>')
class CategoryById(MethodView):
    '''
    Routes to:
        Update an existing category
        Delete an existing category
    '''

    def put(self, category_id):
        'Update an existing category'

    def delete(self, category_id):
        'Delete an existing category'

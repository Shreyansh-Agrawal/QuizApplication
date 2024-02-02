'Routes for the Category related functionalities'

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from config.string_constants import Roles
from controllers.category_controller import CategoryController
from database.database_access import DatabaseAccess
from schemas.category import (
    CategoryResponseSchema,
    CategorySchema,
    CategoryUpdateSchema
)
from schemas.config_schema import ResponseSchema
from utils.rbac import access_level

blp = Blueprint('Category', __name__, description='Routes for the Category related functionalities')

db = DatabaseAccess()
category_controller = CategoryController(db)


@blp.route('/categories')
class Category(MethodView):
    '''
    Routes to:
        Get all categories details
        Create a new category
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    @blp.response(200, CategoryResponseSchema)

    def get(self):
        'Get all categories details'
        return category_controller.get_all_categories()

    @access_level(roles=[Roles.ADMIN])
    @blp.arguments(CategorySchema)
    @blp.response(201, ResponseSchema)

    def post(self, category_data):
        'Create a new category'
        user_id = get_jwt_identity()
        return category_controller.create_category(category_data, user_id)


@blp.route('/categories/<string:category_id>')
class CategoryById(MethodView):
    '''
    Routes to:
        Update an existing category
        Delete an existing category
    '''

    @access_level(roles=[Roles.ADMIN])
    @blp.arguments(CategoryUpdateSchema)
    @blp.response(200, ResponseSchema)

    def put(self, category_data, category_id):
        'Update an existing category'
        return category_controller.update_category(category_data, category_id)

    @access_level(roles=[Roles.ADMIN])
    @blp.response(200, ResponseSchema)

    def delete(self, category_id):
        'Delete an existing category'
        return category_controller.delete_category(category_id)

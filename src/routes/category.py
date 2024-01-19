'Routes for the Category related functionalities'

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint, abort

from config.message_prompts import Roles
from controllers.category import CategoryController
from controllers.user import UserController
from database.database_access import DatabaseAccess
from schemas.category import CategorySchema, CategoryUpdateSchema
from utils.custom_error import DuplicateEntryError
from utils.rbac import access_level

blp = Blueprint('Category', __name__, description='Routes for the Category related functionalities')

db = DatabaseAccess()
category_controller = CategoryController(db)
user_controller = UserController(db)


@blp.route('/categories')
class Category(MethodView):
    '''
    Routes to:
        Get all categories details
        Create a new category
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        'Get all categories details'

        category_data = category_controller.get_all_categories()
        if not category_data:
            abort(404, message='No category present')
        return category_data

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    @blp.arguments(CategorySchema)
    def post(self, category_data):
        'Create a new category'

        username = get_jwt_identity()
        data = user_controller.get_user_id(username)
        user_id = data[0].get('user_id')
        try:
            category_data['admin_id'] = user_id
            category_data['admin_username'] = username
            category_controller.create_category(category_data)
        except DuplicateEntryError as e:
            abort(409, message=str(e))

        return {'message': f"Category: {category_data.get('category_name')} created successfully"}, 201


@blp.route('/categories/<string:category_id>')
class CategoryById(MethodView):
    '''
    Routes to:
        Update an existing category
        Delete an existing category
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    @blp.arguments(CategoryUpdateSchema)
    def put(self, category_data, category_id):
        'Update an existing category'

        updated_category_name = category_data.get('updated_category_name')
        try:
            category_controller.update_category(category_id, updated_category_name)
        except DuplicateEntryError as e:
            abort(409, message=str(e))

        return {'message': "Category updated successfully"}

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def delete(self, category_id):
        'Delete an existing category'

        category_controller.delete_category(category_id)
        return {'message': "Category deleted successfully"}

'Routes for the User related functionalities'

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint, abort

from config.message_prompts import Roles
from controllers.user import UserController
from database.database_access import DatabaseAccess
from schemas.user import UserSchema, UserUpdateSchema
from utils.custom_error import DuplicateEntryError
from utils.rbac import access_level

blp = Blueprint('User', __name__, description='Routes for the User related functionalities')

db = DatabaseAccess()
user_controller = UserController(db)


@blp.route('/users/profile')
class UserById(MethodView):
    '''
    Routes to:
        View user profile
        Update user profile
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    @blp.response(200, UserSchema)
    def get(self):
        'Get user profile data'

        user_id = get_jwt_identity()
        user_data = user_controller.get_user_profile_data(user_id)
        if not user_data:
            abort(404, message='User data not found')
        return user_data[0]

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    @blp.arguments(UserUpdateSchema)
    def patch(self, user_data):
        'Update user profile'

        user_id = get_jwt_identity()
        try:
            user_controller.update_user_data(user_id, user_data)
        except DuplicateEntryError as e:
            abort(409, message=str(e))
        return {'message': 'Profile updated successfully'}, 200


@blp.route('/players')
class Player(MethodView):
    '''
    Routes to:
        Get all player details
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    @blp.response(200, UserSchema(many=True))
    def get(self):
        'Get all player details'

        player_data = user_controller.get_all_users_by_role(role=Roles.PLAYER)
        if not player_data:
            abort(404, message='No players exist')
        return player_data


@blp.route('/admins')
class Admin(MethodView):
    '''
    Routes to:
        Get all admins details
        Create a new admin account
    '''

    @access_level(roles=[Roles.SUPER_ADMIN])
    @blp.response(200, UserSchema(many=True))
    def get(self):
        'Get all admin details'

        admin_data = user_controller.get_all_users_by_role(role=Roles.ADMIN)
        if not admin_data:
            abort(404, message='No admins exist')
        return admin_data

    @access_level(roles=[Roles.SUPER_ADMIN])
    @blp.arguments(UserSchema)
    def post(self, admin_data):
        'Create a new admin account'
        try:
            user_controller.create_admin(admin_data)
        except DuplicateEntryError as e:
            abort(409, message=str(e))

        return {'message': 'Admin created successfully'}, 201


@blp.route('/admins/<string:admin_id>')
class AdminById(MethodView):
    '''
    Routes to:
        Delete an existing admin
    '''

    @access_level(roles=[Roles.SUPER_ADMIN])
    def delete(self, admin_id):
        'Delete an existing admin'

        row_affected = user_controller.delete_admin_by_id(admin_id)
        if not row_affected:
            abort(404, message='Admin does not exists')
        return {'message': "Admin deleted successfully"}


@blp.route('/players/<string:player_id>')
class PlayerById(MethodView):
    '''
    Routes to:
        Delete an existing player
    '''

    @access_level(roles=[Roles.ADMIN])
    def delete(self, player_id):
        'Delete an existing player'

        row_affected = user_controller.delete_player_by_id(player_id)
        if not row_affected:
            abort(404, message='Player does not exists')
        return {'message': "Player deleted successfully"}

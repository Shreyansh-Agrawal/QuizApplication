'Routes for the User related functionalities'

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from config.message_prompts import Roles
from controllers.user_controller import UserController
from database.database_access import DatabaseAccess
from schemas.user import UserSchema, UserUpdateSchema, PasswordUpdateSchema
from utils.rbac import access_level

blp = Blueprint('User', __name__, description='Routes for the User related functionalities')

db = DatabaseAccess()
user_controller = UserController(db)


@blp.route('/profile/me')
class Profile(MethodView):
    '''
    Routes to:
        View user profile
        Update user profile
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    def get(self):
        'Get user profile data'
        user_id = get_jwt_identity()
        return user_controller.get_user_profile_data(user_id)

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    @blp.arguments(UserUpdateSchema)
    def put(self, user_data):
        'Update user profile'
        user_id = get_jwt_identity()
        return user_controller.update_user_data(user_id, user_data)


@blp.route('/profile/password/me')
class Password(MethodView):
    '''
    Routes to:
        Update user password
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    @blp.arguments(PasswordUpdateSchema)
    def put(self, password_data):
        'Update user password'
        user_id = get_jwt_identity()
        return user_controller.update_user_password(user_id, password_data)


@blp.route('/players')
class Player(MethodView):
    '''
    Routes to:
        Get all player details
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def get(self):
        'Get all player details'
        return user_controller.get_all_players()


@blp.route('/admins')
class Admin(MethodView):
    '''
    Routes to:
        Get all admins details
        Create a new admin account
    '''

    @access_level(roles=[Roles.SUPER_ADMIN])
    def get(self):
        'Get all admin details'
        return user_controller.get_all_admins()


    @access_level(roles=[Roles.SUPER_ADMIN])
    @blp.arguments(UserSchema)
    def post(self, admin_data):
        'Create a new admin account'
        return user_controller.create_admin(admin_data)


@blp.route('/admins/<string:admin_id>')
class AdminById(MethodView):
    '''
    Routes to:
        Delete an existing admin
    '''

    @access_level(roles=[Roles.SUPER_ADMIN])
    def delete(self, admin_id):
        'Delete an existing admin'
        return user_controller.delete_admin_by_id(admin_id)


@blp.route('/players/<string:player_id>')
class PlayerById(MethodView):
    '''
    Routes to:
        Delete an existing player
    '''

    @access_level(roles=[Roles.ADMIN])
    def delete(self, player_id):
        'Delete an existing player'
        return user_controller.delete_player_by_id(player_id)

'Routes for the User related functionalities'

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from config.message_prompts import Roles
from controllers.user import UserController
from database.database_access import DatabaseAccess
from schemas.user import UserSchema
from utils.custom_error import LoginError
from utils.rbac import access_level

blp = Blueprint('User', __name__, description='Routes for the User related functionalities')

db = DatabaseAccess()
user_controller = UserController(db)


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
        except LoginError as e:
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

        user_controller.delete_user_by_id(admin_id)
        return {'message': "Admin deleted successfully"}

@blp.route('/players/<string:player_id>')
class PlayerById(MethodView):
    '''
    Routes to:
        Delete an existing player
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def delete(self, player_id):
        'Delete an existing player'

        user_controller.delete_user_by_id(player_id)
        return {'message': "Player deleted successfully"}

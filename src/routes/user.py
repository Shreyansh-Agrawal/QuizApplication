'Routes for the User related functionalities'

from flask.views import MethodView
from flask_smorest import Blueprint

from config.message_prompts import Roles
from utils.rbac import access_level

blp = Blueprint('User', __name__, description='Routes for the User related functionalities')


@blp.route('/players')
class Player(MethodView):
    '''
    Routes to:
        Get all player details
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def get(self):
        'Get all player details'


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

    @access_level(roles=[Roles.SUPER_ADMIN])
    def post(self):
        'Create a new admin account'


@blp.route('/admins/<string:admin_id>')
class AdminById(MethodView):
    '''
    Routes to:
        Delete an existing admin
    '''

    @access_level(roles=[Roles.SUPER_ADMIN])
    def delete(self, admin_id):
        'Delete an existing admin'


@blp.route('/players/<string:player_id>')
class PlayerById(MethodView):
    '''
    Routes to:
        Delete an existing player
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
    def delete(self, admin_id):
        'Delete an existing player'

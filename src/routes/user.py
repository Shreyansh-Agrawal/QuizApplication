'Routes for the User related functionalities'

from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint('User', __name__)


@blp.route('/players')
class Player(MethodView):
    '''
    Routes to:
        Get all player details
    '''

    def get(self):
        'Get all player details'


@blp.route('/admins')
class Admin(MethodView):
    '''
    Routes to:
        Get all admins details
        Create a new admin account
    '''

    def get(self):
        'Get all admin details'

    def post(self):
        'Create a new admin account'


@blp.route('/admins/<string:admin_id>')
class AdminById(MethodView):
    '''
    Routes to:
        Delete an existing admin
    '''

    def delete(self, admin_id):
        'Delete an existing admin'


@blp.route('/players/<string:player_id>')
class PlayerById(MethodView):
    '''
    Routes to:
        Delete an existing player
    '''

    def delete(self, admin_id):
        'Delete an existing player'

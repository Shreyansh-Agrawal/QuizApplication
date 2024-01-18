'Routes for the Authentication related functionalities'

from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint('Auth', __name__)


@blp.route('/register')
class Register(MethodView):
    'Routes to register a new user'

    def post(self):
        'Register a new user'


@blp.route('/login')
class Login(MethodView):
    'Routes to login an existing user'

    def post(self):
        'Login an existing user'


@blp.route('/logout')
class Logout(MethodView):
    'Routes to logout a logged in user'

    def post(self):
        'Logout a logged in user'


@blp.route('/refresh')
class Refresh(MethodView):
    'Routes to get a non fresh access token'

    def post(self):
        'Issue a non fresh access token'

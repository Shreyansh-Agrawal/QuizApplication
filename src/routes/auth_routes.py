'Routes for the Authentication related functionalities'

from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint

from controllers.auth_controller import AuthController
from database.database_access import DatabaseAccess
from schemas.auth import LoginSchema, RegistrationSchema

blp = Blueprint('Auth', __name__, description='Routes for the Authentication related functionalities')

db = DatabaseAccess()
auth_controller = AuthController(db)


@blp.route('/register')
class Register(MethodView):
    'Routes to register a new user'

    @blp.arguments(RegistrationSchema)
    def post(self, player_data):
        'Register a new user'
        return auth_controller.register(player_data)


@blp.route('/login')
class Login(MethodView):
    'Routes to login an existing user'

    @blp.arguments(LoginSchema)
    def post(self, login_data):
        'Login an existing user'
        return auth_controller.login(login_data)


@blp.route('/logout')
class Logout(MethodView):
    'Routes to logout a logged in user'

    @jwt_required()
    def post(self):
        'Logout a logged in user'
        jti = get_jwt().get('jti')
        return auth_controller.logout(jti)


@blp.route('/refresh')
class Refresh(MethodView):
    'Routes to get a non fresh access token'

    @jwt_required(refresh=True)
    def post(self):
        'Issue a non fresh access token'
        claims = get_jwt()
        user_id = claims.get('sub')
        mapped_role = claims.get('cap')
        return auth_controller.refresh(user_id, mapped_role)

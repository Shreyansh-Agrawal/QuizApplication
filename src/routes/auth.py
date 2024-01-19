'Routes for the Authentication related functionalities'

from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required
from flask_smorest import Blueprint, abort

from controllers.auth import AuthController
from database.database_access import DatabaseAccess
from schemas.auth import RegistrationSchema, LoginSchema
from utils.blocklist import BLOCKLIST
from utils.custom_error import LoginError
from utils.rbac import ROLE_MAPPING

blp = Blueprint('Auth', __name__, description='Routes for the Authentication related functionalities')

db = DatabaseAccess()
auth_controller = AuthController(db)


@blp.route('/register')
class Register(MethodView):
    'Routes to register a new user'

    @blp.arguments(RegistrationSchema)
    def post(self, player_data):
        'Register a new user'
        try:
            auth_controller.signup(player_data)
        except LoginError as e:
            abort(409, message=str(e))

        return {'msg': 'Successfully registered'}, 201


@blp.route('/login')
class Login(MethodView):
    'Routes to login an existing user'

    @blp.arguments(LoginSchema)
    def post(self, login_data):
        'Login an existing user'

        username, password = login_data.values()
        user_data = auth_controller.login(username, password)
        if not user_data:
            abort(401, message='Invalid credentials')

        username, role, *_ = user_data
        mapped_role = ROLE_MAPPING.get(role)

        access_token = create_access_token(
            identity=username,
            fresh=True,
            additional_claims={'cap': mapped_role}
        )
        refresh_token = create_refresh_token(
            identity=username,
            additional_claims={'cap': mapped_role}
        )

        return {"access_token": access_token, "refresh_token": refresh_token}


@blp.route('/logout')
class Logout(MethodView):
    'Routes to logout a logged in user'

    @jwt_required()
    def post(self):
        'Logout a logged in user'

        jti = get_jwt().get('jti')
        BLOCKLIST.add(jti)
        return {'msg': 'Successfully logged out'}


@blp.route('/refresh')
class Refresh(MethodView):
    'Routes to get a non fresh access token'

    @jwt_required(refresh=True)
    def post(self):
        'Issue a non fresh access token'

        claims = get_jwt()
        current_user = claims.get('sub')
        new_access_token = create_access_token(
            identity=current_user,
            fresh=False,
            additional_claims={'cap': claims.get('cap')}
        )

        return {"access_token": new_access_token}

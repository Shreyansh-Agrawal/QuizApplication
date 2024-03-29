'Routes for the Authentication related functionalities'

import logging
from flask.views import MethodView
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from config.string_constants import AUTHORIZATION_HEADER, LogMessage

from controllers.auth_controller import AuthController
from database.database_access import DatabaseAccess
from schemas.auth import (
    LoginResponseSchema,
    LoginSchema,
    RefreshResponseSchema,
    RegistrationSchema
)
from schemas.config_schema import ResponseSchema

logger = logging.getLogger(__name__)
blp = Blueprint('Auth', __name__, description='Routes for the Authentication related functionalities')

db = DatabaseAccess()
auth_controller = AuthController(db)


@blp.route('/register')
class Register(MethodView):
    'Routes to register a new user'

    @blp.arguments(RegistrationSchema)
    @blp.response(201, ResponseSchema)

    def post(self, player_data):
        'Register a new user'

        logger.info(LogMessage.FUNCTION_CALL, 'Register.post', __name__)
        return auth_controller.register(player_data)


@blp.route('/login')
class Login(MethodView):
    'Routes to login an existing user'

    @blp.arguments(LoginSchema)
    @blp.response(200, LoginResponseSchema)

    def post(self, login_data):
        'Login an existing user'

        logger.info(LogMessage.FUNCTION_CALL, 'Login.post', __name__)
        return auth_controller.login(login_data)


@blp.route('/logout')
class Logout(MethodView):
    'Routes to logout a logged in user'

    @jwt_required()
    @blp.response(200, ResponseSchema)
    @blp.doc(parameters=[AUTHORIZATION_HEADER])

    def post(self):
        'Logout a logged in user'

        user_id = get_jwt_identity()

        logger.info(LogMessage.FUNCTION_CALL, 'Logout.post', __name__)
        return auth_controller.logout(user_id)


@blp.route('/refresh')
class Refresh(MethodView):
    'Routes to get a non fresh access token'

    @jwt_required(refresh=True)
    @blp.response(200, RefreshResponseSchema)
    @blp.doc(parameters=[AUTHORIZATION_HEADER])

    def post(self):
        'Issue a non fresh access token'

        claims = get_jwt()
        user_id = claims.get('sub')
        mapped_role = claims.get('cap')

        logger.info(LogMessage.FUNCTION_CALL, 'Refresh.post', __name__)
        return auth_controller.refresh(user_id, mapped_role)

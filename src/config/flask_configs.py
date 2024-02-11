'Manages all the configurations for the flask app'

import logging
import os

from flask_jwt_extended import JWTManager
from flask_smorest import Api

from config.string_constants import ErrorMessage, StatusCodes
from database.database_access import DatabaseAccess
from helpers.token_helper import TokenHelper
from routes.auth_routes import blp as AuthBlueprint
from routes.category_routes import blp as CategoryBlueprint
from routes.question_routes import blp as QuestionBlueprint
from routes.quiz_routes import blp as QuizBlueprint
from routes.user_routes import blp as UserBlueprint
from utils.custom_error import CustomError, ValidationError
from utils.error_handlers import (
    handle_bad_request,
    handle_invalid_url,
    handle_internal_server_error,
    handle_validation_error
)
from utils.id_generator import generate_id

logger = logging.getLogger(__name__)
db = DatabaseAccess()
token_helper = TokenHelper(db)
request_id = ''


def set_app_configs(app):
    'configures the flask app'

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Quiz Application"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_REDOC_PATH"] = "/redoc"
    app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_RAPIDOC_PATH"] = "/rapidoc"
    app.config["OPENAPI_RAPIDOC_URL"] = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    app.json.sort_keys = False

    @app.before_request
    def generate_request_id():
        global request_id
        request_id = generate_id(entity='Request', length=6)


def register_error_handlers(app):
    'Register error handlers'

    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(404, handle_invalid_url)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(Exception, handle_internal_server_error)


def set_jwt_configs(app):
    'Register jwt in flask app'

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(_jwt_header, jwt_payload):
        'Checks if the token is present in the blocklist'

        token_id = jwt_payload["jti"]
        token_type = jwt_payload["type"]
        return not token_helper.check_token_status(token_id, token_type)

    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_payload):
        'Returns a custom response if a revoked token is encountered'
        error = CustomError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_REVOKED)

        logger.error(error.message)
        return error.error_info, error.code

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(_jwt_header, _jwt_payload):
        '''
        Returns a custom response when a valid and non-fresh token is 
        used on an endpoint that is marked as fresh=True
        '''
        error = CustomError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_NOT_FRESH)

        logger.error(error.message)
        return error.error_info, error.code

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        'Returns a custom response when an expired token is encountered'
        error = CustomError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_EXPIRED)

        logger.error(error.message)
        return error.error_info, error.code

    @jwt.invalid_token_loader
    def invalid_token_callback(err):
        'Returns a custom response when an invalid token is encountered'
        logger.error(err)

        error = CustomError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_TOKEN)
        return error.error_info, error.code

    @jwt.unauthorized_loader
    def missing_token_callback(err):
        'Returns a custom response when no token is present'
        logger.error(err)

        error = CustomError(status=StatusCodes.UNAUTHORIZED, message=ErrorMessage.MISSING_TOKEN)
        return error.error_info, error.code


def register_blueprints(app):
    'Register blueprints to flask app'

    api = Api(app)
    api.register_blueprint(AuthBlueprint, url_prefix='/v1')
    api.register_blueprint(CategoryBlueprint, url_prefix='/v1')
    api.register_blueprint(QuestionBlueprint, url_prefix='/v1')
    api.register_blueprint(QuizBlueprint, url_prefix='/v1')
    api.register_blueprint(UserBlueprint, url_prefix='/v1')


class CustomFilter(logging.Filter):
    'Overriding logging filter'

    def filter(self, record):
        record.request_id = request_id
        return True

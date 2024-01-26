'''
A Flask-based Python Quiz REST API that facilitates the creation, management, 
and completion of quizzes with a focus on data security and user satisfaction.

This script serves as the entry point for the Quiz API, utilizing Flask to handle 
HTTP requests and responses. It initializes the logging configuration, starts the 
Flask application, and handles exceptions by logging errors.

Functions:
- start_quiz_api: Function to start the Quiz API. 
It initializes the Flask application and sets up the necessary routes for quiz-related functionalities.

Usage:
Ensure all required configurations are set up before running this script. 
Execute this script to start the Quiz API, allowing clients to interact with the quiz functionalities 
through HTTP requests.
'''

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from config.message_prompts import ErrorMessage, LogMessage, StatusCodes
from database.database_access import DatabaseAccess
from routes.auth_routes import blp as AuthBlueprint
from routes.category_routes import blp as CategoryBlueprint
from routes.question_routes import blp as QuestionBlueprint
from routes.quiz_routes import blp as QuizBlueprint
from routes.user_routes import blp as UserBlueprint
from utils.blocklist import BLOCKLIST
from utils.custom_error import CustomError, ValidationError
from utils.error_handlers import handle_internal_server_error, handle_validation_error, handle_bad_request
from utils.initialize_app import Initializer

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

logger = logging.getLogger(__name__)
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


def initialize_quiz_app():
    '''Function to initialize the Application.'''

    logger.info(LogMessage.SYSTEM_START)
    db = DatabaseAccess()
    initializer = Initializer(db)
    try:
        initializer.initialize_app()
    except Exception as e: # pylint: disable=broad-exception-caught
        logger.exception(e)


def create_app():
    '''Creates and configures the flask app'''

    initialize_quiz_app()
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Quiz Application"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_REDOC_PATH"] = "/redoc"
    app.config["OPENAPI_REDOC_URL"] = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_RAPIDOC_PATH"] = "/rapidoc"
    app.config["OPENAPI_RAPIDOC_URL"] = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(ValidationError, handle_validation_error)
    # app.register_error_handler(Exception, handle_internal_server_error)

    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(_jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_payload):
        error = CustomError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_REVOKED)
        return error.error_info, error.code

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(_jwt_header, _jwt_payload):
        error = CustomError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_NOT_FRESH)
        return error.error_info, error.code

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        error = CustomError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_EXPIRED)
        return error.error_info, error.code

    @jwt.invalid_token_loader
    def invalid_token_callback(_error):
        error = CustomError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.INVALID_TOKEN)
        return error.error_info, error.code

    @jwt.unauthorized_loader
    def missing_token_callback(_error):
        error = CustomError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.MISSING_TOKEN)
        return error.error_info, error.code

    api.register_blueprint(AuthBlueprint, url_prefix='/v1')
    api.register_blueprint(CategoryBlueprint, url_prefix='/v1')
    api.register_blueprint(QuestionBlueprint, url_prefix='/v1')
    api.register_blueprint(QuizBlueprint, url_prefix='/v1')
    api.register_blueprint(UserBlueprint, url_prefix='/v1')

    return app


flask_app = create_app()

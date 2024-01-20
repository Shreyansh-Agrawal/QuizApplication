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
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from config.message_prompts import LogMessage
from database.database_access import DatabaseAccess
from routes.auth import blp as AuthBlueprint
from routes.category import blp as CategoryBlueprint
from routes.question import blp as QuestionBlueprint
from routes.quiz import blp as QuizBlueprint
from routes.user import blp as UserBlueprint
from utils.blocklist import BLOCKLIST
from utils.error_handlers import handle_internal_server_error
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


def create_app():
    '''Creates and configures the flask app'''

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

    app.register_error_handler(Exception, handle_internal_server_error)

    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(_jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(_jwt_header, _jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(_error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(_error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(AuthBlueprint, url_prefix='/v1')
    api.register_blueprint(CategoryBlueprint, url_prefix='/v1')
    api.register_blueprint(QuestionBlueprint, url_prefix='/v1')
    api.register_blueprint(QuizBlueprint, url_prefix='/v1')
    api.register_blueprint(UserBlueprint, url_prefix='/v1')

    return app


def start_quiz_app():
    '''
    Function to start the Application.

    This function serves as the entry point to the Quiz API. 
    It initializes the Flask application and sets up the necessary components 
    for handling HTTP requests. It then starts the application, allowing clients 
    to interact with the quiz functionalities through the defined API routes.

    Returns:
        None
    '''
    logger.info(LogMessage.SYSTEM_START)
    db = DatabaseAccess()
    initializer = Initializer(db)
    try:
        initializer.initialize_app()
        app = create_app()
        app.run(debug=True)
    except Exception as e: # pylint: disable=broad-exception-caught
        logger.exception(e)

    logger.info(LogMessage.SYSTEM_STOP)


if __name__ == '__main__':
    start_quiz_app() # pragma: no cover

'''
A Flask-based Python Quiz REST API that facilitates the creation, management, 
and completion of quizzes with a focus on data security and user satisfaction.

This script serves as the entry point for the Quiz API, utilizing Flask to handle 
HTTP requests and responses. It initializes the logging configuration, starts the 
Flask application, and handles exceptions by logging errors.

Functions:
- create_app(): Function to start the Quiz API. 
It initializes the Flask application and sets up the necessary routes for quiz-related functionalities.

Usage:
Ensure all required configurations are set up before running this script. 
Execute this script to start the Quiz API, allowing clients to interact with the quiz functionalities 
through HTTP requests.
'''

import logging
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from config.flask_configs import (
    register_blueprints,
    register_error_handlers,
    set_app_configs,
    set_jwt_configs
)
from config.initialize_app import Initializer
from config.message_prompts import LogMessage
from database.database_access import DatabaseAccess

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

logger = logging.getLogger(__name__)
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
db = DatabaseAccess()


def create_app():
    '''Creates and configures the flask app'''

    logger.info(LogMessage.SYSTEM_START)

    Initializer(db).initialize_app()
    app = Flask(__name__)

    set_app_configs(app)
    register_error_handlers(app)
    set_jwt_configs(app)
    register_blueprints(app)

    return app

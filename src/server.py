'''
A FastAPI-based Python Quiz REST API that facilitates the creation, management, 
and completion of quizzes with a focus on data security and user satisfaction.

This script serves as the entry point for the Quiz API, utilizing FastAPI to handle 
HTTP requests and responses. It initializes the logging configuration, starts the 
FastAPI application, and handles exceptions by logging errors.

Functions:
- start_quiz_api: Function to start the Quiz API. 
It initializes the FastAPI application and sets up the necessary routes for quiz-related functionalities.

Usage:
Ensure all required configurations are set up before running this script. 
Execute this script to start the Quiz API, allowing clients to interact with the quiz functionalities 
through HTTP requests.
'''

import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from config.message_prompts import LogMessage
from database.database_access import DatabaseAccess
from routes.auth_routes import router as AuthRouter
from routes.category_routes import router as CategoryRouter
from routes.question_routes import router as QuestionRouter
from routes.quiz_routes import router as QuizRouter
from routes.user_routes import router as UserRouter
from utils.error_handlers import handle_http_exception, handle_internal_server_error, handle_validation_error
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
    '''Creates and configures the FastAPI app'''

    initialize_quiz_app()
    app = FastAPI()

    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(Exception, handle_internal_server_error)

    app.include_router(AuthRouter, prefix='/v1')
    app.include_router(CategoryRouter, prefix='/v1')
    app.include_router(QuestionRouter, prefix='/v1')
    app.include_router(QuizRouter, prefix='/v1')
    app.include_router(UserRouter, prefix='/v1')

    return app


fastapi_app = create_app()

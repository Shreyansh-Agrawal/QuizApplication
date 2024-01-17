'''
A console-based Python Quiz Application that enables users to create, 
manage, and take quizzes efficiently while ensuring data security and user satisfaction.

This script serves as the entry point for a console-based quiz application. 
It initializes the logging configuration, starts the application, and handles exceptions logging errors.

Functions:
- start_quiz_app: Function to start the Application. 
It initializes the application and begins the main menu for user interaction.

Usage:
Ensure all necessary configurations are set up before running this script. 
Execute this script to start the quiz application.
'''

import logging

from config.message_prompts import DisplayMessage, LogMessage
from database.database_access import DatabaseAccess
from menu.main_menu import MainMenu
from utils.initialize_app import Initializer

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

logger = logging.getLogger(__name__)


def start_quiz_app():
    '''
    Function to start the Application.

    This function serves as the entry point to the quiz application. 
    It initiates the application by calling Initializer.initialize_app() to set up essential components and 
    MainMenu.auth_menu() to display the main menu for user interaction.

    Returns:
        None
    '''
    logger.info(LogMessage.SYSTEM_START)
    db = DatabaseAccess()
    initializer = Initializer(db)
    try:
        initializer.initialize_app()
        MainMenu.auth_menu()
    except Exception as e: # pylint: disable=broad-exception-caught
        logger.exception(e)
        print(f'exception caught in app.py: {e}')
    finally:
        db.connection.close()

    logger.info(LogMessage.SYSTEM_STOP)
    print(DisplayMessage.EXIT_MSG)


if __name__ == '__main__':
    start_quiz_app() # pragma: no cover

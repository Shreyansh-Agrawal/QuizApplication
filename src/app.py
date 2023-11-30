'''
    A console-based Python quiz application that enables users to create, 
    manage, and take quizzes efficiently while ensuring data security and user satisfaction

    Entry point of the application
'''

import logging

from config.message_prompts import DisplayMessage, LogMessage
from utils.initialize_app import Initializer
from menu.main_menu import MainMenu

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

logger = logging.getLogger(__name__)


def start_quiz_app():
    '''Function to start the Application.'''

    logger.info(LogMessage.SYSTEM_START)
    try:
        Initializer.initialize_app()
        MainMenu.auth_menu()
    except Exception as e: # pylint: disable=broad-exception-caught
        logger.exception(e)
        print(e)

    logger.info(LogMessage.SYSTEM_STOP)
    print(DisplayMessage.EXIT_MSG)


if __name__ == '__main__':
    start_quiz_app() # pragma: no cover

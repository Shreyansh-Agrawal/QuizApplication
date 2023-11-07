'''
    A console-based Python quiz application that enables users to create, 
    manage, and take quizzes efficiently while ensuring data security and user satisfaction

    Entry point of the application
'''

import logging

from config.display_menu import DisplayMessage
from utils.initialize_app import Initializer
from utils.menu import start

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('app.py running')

    try:
        Initializer.initialize_app()
        start()
    except Exception as e:
        logger.exception(e)
        print(e)

    logger.info('Stopping Application')
    print(DisplayMessage.EXIT_MSG)

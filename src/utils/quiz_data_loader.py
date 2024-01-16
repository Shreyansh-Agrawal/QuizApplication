'''Functions to load data to database from json file'''

import json
import logging
import mysql.connector

from config.file_paths import FilePaths
from config.message_prompts import LogMessage
from config.queries import Queries
from database.database_access import db
from utils import validations

logger = logging.getLogger(__name__)


def load_quiz_data(admin_username: str) -> None:
    '''
    Loads quiz data to the database from a JSON file.

    Args:
        admin_username (str): The username of the admin who created the quiz.

    Reads JSON data from the specified file path and loads it into the database.
    The JSON file should contain quiz-related information such as questions, categories,
    and options.

    Returns:
        None
    '''
    logger.debug(LogMessage.LOAD_QUIZ_DATA_FROM_JSON)
    admin_data = db.read(Queries.GET_USER_ID_BY_USERNAME, (admin_username, ))
    admin_id = admin_data[0][0]

    with open(FilePaths.QUIZ_DATA_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for category_data in data['quiz_data']:
        category_id = validations.validate_id(entity='category')
        category_name = category_data['category']

        try:
            db.write(Queries.INSERT_CATEGORY, (category_id, admin_id, admin_username, category_name))
        except mysql.connector.IntegrityError as e:
            logger.debug(e)

        for question_data in category_data['question_data']:
            question_id = validations.validate_id(entity='question')
            question_text = question_data['question_text']
            question_type = question_data['question_type'].upper()

            answer_id = validations.validate_id(entity='option')
            answer_text = question_data['options']['answer']

            try:
                db.write(
                    Queries.INSERT_QUESTION,
                    (question_id, category_id, admin_id, admin_username, question_text, question_type)
                )
                db.write(Queries.INSERT_OPTION, (answer_id, question_id, answer_text, 1))

                if question_type.lower() == 'mcq':
                    for i in range(3):
                        other_option_id = validations.validate_id(entity='option')
                        other_option = question_data['options']['other_options'][i]

                        db.write(Queries.INSERT_OPTION, (other_option_id, question_id, other_option, 0))
            except mysql.connector.IntegrityError as e:
                logger.debug(e)

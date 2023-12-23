'''Functions to load data to database from json file'''

import json
import logging
import sqlite3

from config.file_paths import FilePaths
from config.message_prompts import LogMessage
from config.queries import Queries
from database.database_access import dao
from utils import validations

logger = logging.getLogger(__name__)


def load_quiz_data_from_json(created_by_admin_username: str) -> None:
    '''
    Loads quiz data to the database from a JSON file.

    Args:
        created_by_admin_username (str): The username of the admin who created the quiz.

    Reads JSON data from the specified file path and loads it into the database.
    The JSON file should contain quiz-related information such as questions, categories,
    and options.

    Returns:
        None
    '''
    logger.debug(LogMessage.LOAD_QUIZ_DATA_FROM_JSON)
    admin_data = dao.read_from_database(
                    Queries.GET_USER_ID_BY_USERNAME,
                    (created_by_admin_username, )
                )
    created_by_admin_id = admin_data[0][0]

    with open(FilePaths.QUESTIONS_JSON_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for question in data['questions']:
        question_id = question['question_id']
        question_text = question['question_text']
        question_type = question['question_type'].upper()
        category_id = question['category_id']
        category = question['category']
        admin_id = created_by_admin_id
        admin_username = created_by_admin_username
        answer_id = validations.validate_id(entity='option')
        answer = question['options']['answer']['text']

        try:
            dao.write_to_database(
                Queries.INSERT_CATEGORY,
                (category_id, admin_id, admin_username, category))

        except sqlite3.IntegrityError:
            # Not logging the error: Reason - Definite error due to json data structure
            pass

        try:
            dao.write_to_database(
                Queries.INSERT_QUESTION,
                (question_id, category_id, admin_id, admin_username, question_text, question_type))

            dao.write_to_database(
                Queries.INSERT_OPTION,
                (answer_id, question_id, answer, 1))

            if question_type.lower() == 'mcq':
                for i in range(3):
                    other_option_id = validations.validate_id(entity='option')
                    other_option = question['options']['other_options'][i]['text']

                    dao.write_to_database(
                        Queries.INSERT_OPTION,
                        (other_option_id, question_id, other_option, 0))

        except sqlite3.IntegrityError:
            # Not logging the error: Reason - Definite error due to json data structure
            pass

'''Functions to load data to database from json file'''

import json
import sqlite3

from config.queries import Queries
from database.database_access import DatabaseAccess as DAO
from utils import validations


def load_questions_from_json(created_by_admin_username: str) -> None:
    '''Function to load data to db from json'''

    admin_data = DAO.read_from_database(
                    Queries.GET_USER_ID_BY_USERNAME,
                    (created_by_admin_username, )
                )
    created_by_admin_id = admin_data[0][0]

    with open('src\\config\\questions.json', 'r', encoding="utf-8") as file:
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
            DAO.write_to_database(
                Queries.INSERT_CATEGORY,
                (category_id, admin_id, admin_username, category))

        except sqlite3.IntegrityError:
            pass

        try:
            DAO.write_to_database(
                Queries.INSERT_QUESTION,
                (question_id, category_id, admin_id, admin_username, question_text, question_type))

            DAO.write_to_database(
                Queries.INSERT_OPTION,
                (answer_id, question_id, answer, 1))

            if question_type.lower() == 'mcq':
                for i in range(3):
                    other_option_id = validations.validate_id(entity='option')
                    other_option = question['options']['other_options'][i]['text']

                    DAO.write_to_database(
                        Queries.INSERT_OPTION,
                        (other_option_id, question_id, other_option, 0))

        except sqlite3.IntegrityError:
            pass

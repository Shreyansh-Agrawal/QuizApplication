'''Contains classes for Quiz, Category, Question and Option'''

from abc import ABC
from typing import Dict
from config.message_prompts import ErrorMessage

from config.queries import Queries
from database.database_access import DatabaseAccess as DAO
from models.database_saver import DatabaseSaver
from utils import validations
from utils.custom_error import DataNotFoundError


class QuizEntity(ABC):
    '''Abstract Base Class'''

    def __init__(self, text: str, quiz_entity: str) -> None:
        self.text = text
        self.entity_id = validations.validate_id(entity=quiz_entity)


class Category(QuizEntity, DatabaseSaver):
    '''Category Class'''

    def __init__(self, category_data: Dict) -> None:
        super().__init__(category_data.get('category_name'), quiz_entity='category')
        self.admin_id = category_data.get('admin_id')
        self.admin_username = category_data.get('admin_username')

    def save_to_database(self) -> None:
        '''method to add category to database'''

        category_data = (
            self.entity_id,
            self.admin_id,
            self.admin_username,
            self.text
        )

        DAO.write_to_database(Queries.INSERT_CATEGORY, category_data)


class Option(QuizEntity, DatabaseSaver):
    '''Option Class'''

    def __init__(self, option_data: Dict) -> None:
        super().__init__(option_data.get('option_text'), quiz_entity='option')
        self.question_id = option_data.get('question_id')
        self.is_correct = option_data.get('is_correct')

    def save_to_database(self) -> None:
        '''method to add option to database'''

        option_data = (
            self.entity_id,
            self.question_id,
            self.text,
            self.is_correct
        )

        DAO.write_to_database(Queries.INSERT_OPTION, option_data)


class Question(QuizEntity, DatabaseSaver):
    '''Question Class'''

    def __init__(self, question_data: Dict) -> None:
        super().__init__(question_data.get('question_text'), quiz_entity='question')
        self.category_id = question_data.get('category_id')
        self.admin_id = question_data.get('admin_id')
        self.admin_username = question_data.get('admin_username')
        self.question_type = question_data.get('question_type')
        self.options = []

    def add_option(self, option: Option) -> None:
        '''method to add option objects'''

        self.options.append(option)

    def save_to_database(self) -> None:
        '''method to add question and its option to database'''

        question_data = (
            self.entity_id,
            self.category_id,
            self.admin_id,
            self.admin_username,
            self.text,
            self.question_type
        )

        if not self.options:
            raise DataNotFoundError(ErrorMessage.NO_OPTIONS_ERROR)

        DAO.write_to_database(Queries.INSERT_QUESTION, question_data)

        for option in self.options:
            option.save_to_database()

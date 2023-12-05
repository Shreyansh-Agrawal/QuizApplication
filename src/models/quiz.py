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
    '''
    Abstract Base Class for Quiz Entities.

    Attributes:
        text (str): The text or content of the quiz entity.
        entity_id (str): The unique identifier for the quiz entity.
    '''

    def __init__(self, text: str, quiz_entity: str) -> None:
        '''
        Initializes a QuizEntity instance.

        Args:
            text (str): The text or content of the quiz entity.
            quiz_entity (str): The type of quiz entity (category, option, question).
        '''

        self.text = text
        self.entity_id = validations.validate_id(entity=quiz_entity)


class Category(QuizEntity, DatabaseSaver):
    '''
    Class representing a Category in the quiz.

    Inherits from:
        QuizEntity: Abstract Base Class for Quiz Entities.
        DatabaseSaver: Interface for saving to the database.

    Methods:
        save_to_database(): Adds the category to the database.
    '''

    def __init__(self, category_data: Dict) -> None:
        '''
        Initializes a Category instance.

        Args:
            category_data (Dict): A dictionary containing category details.
        '''

        super().__init__(category_data.get('category_name'), quiz_entity='category')
        self.admin_id = category_data.get('admin_id')
        self.admin_username = category_data.get('admin_username')

    def save_to_database(self) -> None:
        '''Adds the category to the database.'''

        category_data = (
            self.entity_id,
            self.admin_id,
            self.admin_username,
            self.text
        )

        DAO.write_to_database(Queries.INSERT_CATEGORY, category_data)


class Option(QuizEntity, DatabaseSaver):
    '''
    Class representing an Option for a question in the quiz.

    Inherits from:
        QuizEntity: Abstract Base Class for Quiz Entities.
        DatabaseSaver: Interface for saving to the database.

    Methods:
        save_to_database(): Adds the option to the database.
    '''

    def __init__(self, option_data: Dict) -> None:
        '''
        Initializes an Option instance.

        Args:
            option_data (Dict): A dictionary containing option details.
        '''

        super().__init__(option_data.get('option_text'), quiz_entity='option')
        self.question_id = option_data.get('question_id')
        self.is_correct = option_data.get('is_correct')

    def save_to_database(self) -> None:
        '''Adds the option to the database.'''

        option_data = (
            self.entity_id,
            self.question_id,
            self.text,
            self.is_correct
        )

        DAO.write_to_database(Queries.INSERT_OPTION, option_data)


class Question(QuizEntity, DatabaseSaver):
    '''
    Class representing a Question in the quiz.

    Inherits from:
        QuizEntity: Abstract Base Class for Quiz Entities.
        DatabaseSaver: Interface for saving to the database.

    Methods:
        add_option(): Adds an option object to the question.
        save_to_database(): Adds the question and its options to the database.
    '''

    def __init__(self, question_data: Dict) -> None:
        '''
        Initializes a Question instance.

        Args:
            question_data (Dict): A dictionary containing question details.
        '''

        super().__init__(question_data.get('question_text'), quiz_entity='question')
        self.category_id = question_data.get('category_id')
        self.admin_id = question_data.get('admin_id')
        self.admin_username = question_data.get('admin_username')
        self.question_type = question_data.get('question_type')
        self.options = []

    def add_option(self, option: Option) -> None:
        '''Adds an option object to the question.'''

        self.options.append(option)

    def save_to_database(self) -> None:
        '''Adds the question and its options to the database.'''

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

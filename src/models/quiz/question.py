'''Contains Question Class'''

from typing import Dict
from config.message_prompts import ErrorMessage

from config.queries import Queries
from models.database.database_access import db
from models.database.database_saver import DatabaseSaver
from models.quiz.quiz_entity import QuizEntity
from models.quiz.option import Option
from utils.custom_error import DataNotFoundError


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

        db.write_to_database(Queries.INSERT_QUESTION, question_data)

        for option in self.options:
            option.save_to_database()

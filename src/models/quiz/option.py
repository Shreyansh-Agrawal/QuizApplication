'''Contains classes for Quiz, Category, Question and Option'''

from typing import Dict

from config.queries import Queries
from models.database.database_access import db
from models.database.database_saver import DatabaseSaver
from models.quiz.quiz_entity import QuizEntity


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

        db.write(Queries.INSERT_OPTION, option_data)

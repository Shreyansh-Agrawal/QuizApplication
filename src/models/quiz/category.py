'''Contains classes for Quiz, Category, Question and Option'''

from typing import Dict

from config.queries import Queries
from models.database.database_access import db
from models.database.database_saver import DatabaseSaver
from models.quiz.quiz_entity import QuizEntity


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

        db.write(Queries.INSERT_CATEGORY, category_data)

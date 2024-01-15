'''Contains classes for Quiz, Category, Question and Option'''

from dataclasses import dataclass
from typing import Dict

from config.queries import Queries
from models.database.database_access import db
from models.database.database_saver import DatabaseSaver
from models.quiz.quiz_entity import QuizEntity


@dataclass
class Category(QuizEntity):
    '''
    Class representing a Category in the quiz.

    Inherits from:
        QuizEntity: Abstract Class for Quiz Entities.
    '''
    admin_id: str
    admin_username: str

    @classmethod
    def get_instance(cls, entity_data: Dict[str, str]) -> 'Category':
        '''Factory method to create a new instance of Category class.'''

        return cls(
            text=entity_data.get('category_name'),
            quiz_entity='category',
            admin_id=entity_data.get('admin_id'),
            admin_username=entity_data.get('admin_username')
        )


class CategoryDB(DatabaseSaver):
    '''Class responsible for saving category to database'''

    @classmethod
    def save(cls, entity: Category) -> None:
        '''Adds the category to the database.'''

        category_data = (
            entity.entity_id,
            entity.admin_id,
            entity.admin_username,
            entity.text
        )
        db.write(Queries.INSERT_CATEGORY, category_data)

'''Contains classes for Quiz, Category, Question and Option'''

from dataclasses import dataclass
from typing import Dict

from models.quiz.quiz_entity import QuizEntity


@dataclass
class Category(QuizEntity):
    '''
    Class representing a Category in the quiz.

    Inherits from:
        QuizEntity: Abstract Class for Quiz Entities.
    '''
    admin_id: str

    @classmethod
    def get_instance(cls, entity_data: Dict[str, str]) -> 'Category':
        '''Factory method to create a new instance of Category class.'''

        return cls(
            text=entity_data.get('category_name'),
            quiz_entity='category',
            admin_id=entity_data.get('admin_id')
        )

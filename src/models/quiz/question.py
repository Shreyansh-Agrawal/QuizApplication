'''Contains Question Class'''

from dataclasses import dataclass
from typing import Dict, List

from models.quiz.option import Option
from models.quiz.quiz_entity import QuizEntity


@dataclass
class Question(QuizEntity):
    '''
    Class representing a Question in the quiz.

    Inherits from:
        QuizEntity: Abstract Base Class for Quiz Entities.

    Methods:
        add_option(): Adds an option object to the question.
    '''
    category_id: str
    admin_id: str
    question_type: str
    options: List

    @classmethod
    def get_instance(cls, entity_data: Dict[str, str]) -> 'Question':
        '''Factory method to create a new instance of Question model.'''

        return cls(
            text=entity_data.get('question_text'),
            quiz_entity='question',
            category_id = entity_data.get('category_id'),
            admin_id = entity_data.get('admin_id'),
            question_type = entity_data.get('question_type'),
            options = []
        )

    def add_option(self, option: Option) -> None:
        '''Adds an option object to the question.'''

        self.options.append(option)

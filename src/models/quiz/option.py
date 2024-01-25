'''Contains classes for Quiz, Category, Question and Option'''

from dataclasses import dataclass
from typing import Dict

from models.quiz.quiz_entity import QuizEntity


@dataclass
class Option(QuizEntity):
    '''
    Class representing an Option for a question in the quiz.

    Inherits from:
        QuizEntity: Abstract Class for Quiz Entities.
    '''
    question_id: str
    is_correct: str

    @classmethod
    def get_instance(cls, entity_data: Dict[str, str]) -> 'Option':
        '''Factory method to create a new instance of Option model.'''

        return cls(
            text=entity_data.get('option_text'),
            quiz_entity='option',
            question_id = entity_data.get('question_id'),
            is_correct = entity_data.get('is_correct')
        )

'''Contains classes for Quiz, Category, Question and Option'''

from abc import ABC
from utils import validations


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

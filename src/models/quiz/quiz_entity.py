'''Contains classes for Quiz, Category, Question and Option'''

from abc import ABC, abstractmethod
from typing import Dict
from dataclasses import dataclass, field

from utils import validations


@dataclass
class QuizEntity(ABC):
    '''
    Abstract Class for Quiz Entities.

    Attributes:
        text (str): The text or content of the quiz entity.
        quiz_entity (str): The name of the quiz entity.
        entity_id (str): The unique identifier for the quiz entity.
    '''
    text: str
    quiz_entity: str
    entity_id: str = field(init=False)

    def __post_init__(self) -> None:
        self.entity_id = validations.validate_id(entity=self.quiz_entity)

    @classmethod
    @abstractmethod
    def get_instance(cls, entity_data: Dict[str, str]) -> 'QuizEntity':
        '''Factory method to create a new instance of QuizEntity class.'''

'''Contains classes for Quiz, Category, Question and Option'''

from dataclasses import dataclass
from typing import Dict

from config.queries import Queries
from models.database.database_access import db
from models.database.database_saver import DatabaseSaver
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
        '''Factory method to create a new instance of Option class.'''

        return cls(
            text=entity_data.get('option_text'),
            quiz_entity='option',
            question_id = entity_data.get('question_id'),
            is_correct = entity_data.get('is_correct')
        )


class OptionDB(DatabaseSaver):
    '''Class responsible for saving option to database'''

    @classmethod
    def save(cls, entity: Option) -> None:
        '''Adds the option to the database.'''

        option_data = (
            entity.entity_id,
            entity.question_id,
            entity.text,
            entity.is_correct
        )

        db.write(Queries.INSERT_OPTION, option_data)

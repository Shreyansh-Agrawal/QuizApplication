'''Contains Question Class'''

from dataclasses import dataclass
from typing import Dict, List

from config.message_prompts import ErrorMessage
from config.queries import Queries
from models.database.database_access import db
from models.database.database_saver import DatabaseSaver
from models.quiz.option import Option, OptionDB
from models.quiz.quiz_entity import QuizEntity
from utils.custom_error import DataNotFoundError


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
    admin_username: str
    question_type: str
    options: List

    @classmethod
    def get_instance(cls, entity_data: Dict[str, str]) -> 'Question':
        '''Factory method to create a new instance of Question class.'''

        return cls(
            text=entity_data.get('question_text'),
            quiz_entity='question',
            category_id = entity_data.get('category_id'),
            admin_id = entity_data.get('admin_id'),
            admin_username = entity_data.get('admin_username'),
            question_type = entity_data.get('question_type'),
            options = []
        )

    def add_option(self, option: Option) -> None:
        '''Adds an option object to the question.'''

        self.options.append(option)


class QuestionDB(DatabaseSaver):
    '''Class responsible for saving question to database'''

    @classmethod
    def save(cls, entity: Question) -> None:
        '''Adds the question to the database.'''

        question_data = (
            entity.entity_id,
            entity.category_id,
            entity.admin_id,
            entity.admin_username,
            entity.text,
            entity.question_type
        )
        if not entity.options:
            raise DataNotFoundError(ErrorMessage.NO_OPTIONS_ERROR)

        db.write(Queries.INSERT_QUESTION, question_data)
        for option in entity.options:
            OptionDB.save(option)

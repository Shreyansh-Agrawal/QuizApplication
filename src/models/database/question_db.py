'''Contains QuestionDB Class'''

from config.message_prompts import ErrorMessage
from config.queries import Queries
from database.database_access import DatabaseAccess
from models.database.database_saver import DatabaseSaver
from models.database.option_db import OptionDB
from models.quiz.question import Question
from utils.custom_error import DataNotFoundError


class QuestionDB(DatabaseSaver):
    '''Class responsible for saving question to database'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.option_db = OptionDB(self.db)

    def save(self, entity: Question) -> None:
        '''Adds the question to the database.'''

        question_data = (
            entity.entity_id,
            entity.category_id,
            entity.admin_id,
            entity.text,
            entity.question_type
        )
        if not entity.options:
            raise DataNotFoundError(ErrorMessage.NO_OPTIONS_ERROR)

        self.db.write(Queries.INSERT_QUESTION, question_data)
        for option in entity.options:
            self.option_db.save(option)

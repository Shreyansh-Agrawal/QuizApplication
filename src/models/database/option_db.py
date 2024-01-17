'''Contains OptionDB Class'''

from config.queries import Queries
from database.database_access import DatabaseAccess
from models.database.database_saver import DatabaseSaver
from models.quiz.option import Option


class OptionDB(DatabaseSaver):
    '''Class responsible for saving option to database'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database

    def save(self, entity: Option) -> None:
        '''Adds the option to the database.'''

        option_data = (
            entity.entity_id,
            entity.question_id,
            entity.text,
            entity.is_correct
        )

        self.db.write(Queries.INSERT_OPTION, option_data)

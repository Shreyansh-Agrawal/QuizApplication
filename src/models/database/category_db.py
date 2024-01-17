'''Contains CategoryDB Class'''

from config.queries import Queries
from database.database_access import DatabaseAccess
from models.database.database_saver import DatabaseSaver
from models.quiz.category import Category


class CategoryDB(DatabaseSaver):
    '''Class responsible for saving category to database'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database

    def save(self, entity: Category) -> None:
        '''Adds the category to the database.'''

        category_data = (
            entity.entity_id,
            entity.admin_id,
            entity.admin_username,
            entity.text
        )
        self.db.write(Queries.INSERT_CATEGORY, category_data)

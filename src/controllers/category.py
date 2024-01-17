'''Controllers for Operations related to Quiz'''

import logging
from typing import Dict, List, Tuple

import mysql.connector

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage
from config.queries import Queries
from database.database_access import DatabaseAccess
from models.quiz.category import Category
from models.database.category_db import CategoryDB
from utils.custom_error import DuplicateEntryError

logger = logging.getLogger(__name__)


class CategoryController:
    '''CategoryController class for category management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.category_db = CategoryDB(self.db)

    def get_all_categories(self) -> List[Tuple]:
        '''Return all Quiz Categories'''

        data = self.db.read(Queries.GET_ALL_CATEGORIES)
        return data

    def create_category(self, category_data: Dict) -> None:
        '''Add a Quiz Category'''

        logger.debug(LogMessage.CREATE_ENTITY, Headers.CATEGORY)
        category = Category.get_instance(category_data)

        try:
            self.category_db.save(category)
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.CATEGORY)) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.CATEGORY)
        print(DisplayMessage.CREATE_CATEGORY_SUCCESS_MSG)

    def update_category_by_name(self, old_category_name: str, new_category_name: str) -> None:
        '''Update a category by category name'''

        logger.debug(LogMessage.UPDATE_ENTITY, Headers.CATEGORY)
        try:
            self.db.write(Queries.UPDATE_CATEGORY_BY_NAME, (new_category_name, old_category_name))
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.CATEGORY)) from e

        logger.debug(LogMessage.UPDATE_CATEGORY_SUCCESS, old_category_name, new_category_name)
        print(
            DisplayMessage.UPDATE_CATEGORY_SUCCESS_MSG.format(
                name=old_category_name, new_name=new_category_name
            )
        )

    def delete_category_by_name(self, category_name: str) -> None:
        '''Delete a category by category name'''

        logger.warning(LogMessage.DELETE_CATEGORY, category_name)
        self.db.write(Queries.DELETE_CATEGORY_BY_NAME, (category_name, ))

        logger.debug(LogMessage.DELETE_CATEGORY_SUCCESS, category_name)
        print(DisplayMessage.DELETE_CATEGORY_SUCCESS_MSG.format(name=category_name))

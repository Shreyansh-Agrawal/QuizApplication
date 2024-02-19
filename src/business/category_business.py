'''Business logic for Operations related to Category'''

import logging
from typing import Dict, List

import pymysql

from config.queries import Queries
from config.string_constants import (
    ErrorMessage,
    Headers,
    LogMessage,
    StatusCodes
)
from database.database_access import DatabaseAccess
from models.quiz.category import Category
from utils.custom_error import DataNotFoundError, DuplicateEntryError

logger = logging.getLogger(__name__)


class CategoryBusiness:
    '''CategoryBusiness class for category management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database

    def get_all_categories(self) -> List[Dict]:
        '''Return all Quiz Categories'''

        logger.info(LogMessage.GET_ALL_CATEGORIES)

        data = self.db.read(Queries.GET_ALL_CATEGORIES)
        if not data:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.NO_CATEGORY)
        return data

    def create_category(self, category_data: Dict) -> None:
        '''Add a Quiz Category'''

        logger.info(LogMessage.CREATE_ENTITY, Headers.CATEGORY)

        category = Category.get_instance(category_data)
        try:
            self.__save_category(category)
        except mysql.connector.IntegrityError as e:
            logger.exception(e)
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.CATEGORY_EXISTS) from e

        logger.info(LogMessage.CREATE_SUCCESS, Headers.CATEGORY)

    def __save_category(self, entity: Category) -> None:
        '''Adds the category to the database.'''

        category_data = (
            entity.entity_id,
            entity.admin_id,
            entity.text
        )
        self.db.write(Queries.INSERT_CATEGORY, category_data)

    def update_category(self, category_id: str, new_category_name: str) -> None:
        '''Update a category name by category id'''

        logger.info(LogMessage.UPDATE_ENTITY, Headers.CATEGORY)

        try:
            row_affected = self.db.write(Queries.UPDATE_CATEGORY_BY_ID, (new_category_name, category_id))
        except mysql.connector.IntegrityError as e:
            logger.exception(e)
            raise DuplicateEntryError(status=StatusCodes.CONFLICT, message=ErrorMessage.CATEGORY_EXISTS) from e
        if not row_affected:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.CATEGORY_NOT_FOUND)

        logger.info(LogMessage.UPDATE_CATEGORY_SUCCESS, category_id, new_category_name)

    def delete_category(self, category_id: str) -> None:
        '''Delete a category by category id'''

        logger.warning(LogMessage.DELETE_CATEGORY, category_id)

        row_affected = self.db.write(Queries.DELETE_CATEGORY_BY_ID, (category_id, ))
        if not row_affected:
            raise DataNotFoundError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.CATEGORY_NOT_FOUND)

        logger.info(LogMessage.DELETE_CATEGORY_SUCCESS, category_id)

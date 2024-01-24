'''Controllers for Operations related to Quiz'''

import logging
from typing import Dict, List, Tuple

from business.category import CategoryBusiness
from config.message_prompts import Message, StatusCodes
from database.database_access import DatabaseAccess
from utils.custom_error import DataNotFoundError, DuplicateEntryError
from utils.success_message import SuccessMessage

logger = logging.getLogger(__name__)


class CategoryController:
    '''CategoryController class for category management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.category_business = CategoryBusiness(self.db)

    def get_all_categories(self) -> List[Tuple]:
        '''Return all Quiz Categories'''

        try:
            category_data = self.category_business.get_all_categories()
        except DataNotFoundError as e:
            return e.error_info, e.code
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=category_data).message_info

    def create_category(self, category_data: Dict, user_id: str) -> None:
        '''Add a Quiz Category'''

        try:
            category_data['admin_id'] = user_id
            self.category_business.create_category(category_data)
        except DuplicateEntryError as e:
            return e.error_info, e.code
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.CREATE_CATEGORY_SUCCESS).message_info

    def update_category(self, category_data: Dict, category_id: str) -> None:
        '''Update a category name by category id'''

        updated_category_name = category_data.get('updated_category_name')
        try:
            self.category_business.update_category(category_id, updated_category_name)
        except DuplicateEntryError as e:
            return e.error_info, e.code
        except DataNotFoundError as e:
            return e.error_info, e.code
        return SuccessMessage(status=StatusCodes.OK, message=Message.UPDATE_CATEGORY_SUCCESS).message_info

    def delete_category(self, category_id: str) -> None:
        '''Delete a category by category id'''

        try:
            self.category_business.delete_category(category_id)
        except DataNotFoundError as e:
            return e.error_info, e.code
        return SuccessMessage(status=StatusCodes.OK, message=Message.DELETE_CATEGORY_SUCCESS).message_info

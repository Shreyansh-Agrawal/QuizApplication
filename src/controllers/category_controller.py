'''Controllers for Operations related to Category'''

import logging
from typing import Dict

from business.category_business import CategoryBusiness
from config.message_prompts import Message, StatusCodes
from database.database_access import DatabaseAccess
from utils.custom_response import SuccessMessage
from utils.error_handlers import handle_custom_errors

logger = logging.getLogger(__name__)


class CategoryController:
    '''CategoryController class for category management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.category_business = CategoryBusiness(self.db)

    @handle_custom_errors
    def get_all_categories(self):
        '''Return all Quiz Categories'''

        category_data = self.category_business.get_all_categories()
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=category_data).message_info

    @handle_custom_errors
    def create_category(self, category_data: Dict, user_id: str):
        '''Add a Quiz Category'''

        category_data['admin_id'] = user_id
        self.category_business.create_category(category_data)
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.CREATE_CATEGORY_SUCCESS).message_info

    @handle_custom_errors
    def update_category(self, category_data: Dict, category_id: str):
        '''Update a category name by category id'''

        updated_category_name = category_data.get('updated_category_name')
        self.category_business.update_category(category_id, updated_category_name)
        return SuccessMessage(status=StatusCodes.OK, message=Message.UPDATE_CATEGORY_SUCCESS).message_info

    @handle_custom_errors
    def delete_category(self, category_id: str):
        '''Delete a category by category id'''

        self.category_business.delete_category(category_id)
        return SuccessMessage(status=StatusCodes.OK, message=Message.DELETE_CATEGORY_SUCCESS).message_info

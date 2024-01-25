'''Controllers for Operations related to Quiz'''

import logging
from typing import List, Tuple, Dict

from business.question import QuestionBusiness
from config.message_prompts import Message, StatusCodes
from database.database_access import DatabaseAccess
from utils.custom_response import SuccessMessage
from utils.error_handlers import handle_custom_errors

logger = logging.getLogger(__name__)


class QuestionController:
    '''QuestionController class for quiz's question management'''

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database
        self.question_business = QuestionBusiness(self.db)

    @handle_custom_errors
    def get_quiz_data(self, category_id: str = None) -> List[Tuple]:
        '''Return the quiz data in a specified category or across all categories'''

        quiz_data = self.question_business.get_quiz_data(category_id)
        return SuccessMessage(status=StatusCodes.OK, message=Message.SUCCESS, data=quiz_data).message_info

    @handle_custom_errors
    def create_question(self, category_id: str, question_data: Dict, admin_id: str) -> None:
        '''Add Questions in a Category'''

        self.question_business.create_question(category_id, question_data, admin_id)
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.QUESTION_CREATED).message_info

    @handle_custom_errors
    def post_quiz_data(self, quiz_data: Dict, admin_id: str) -> None:
        '''Posts quiz data to the database'''

        self.question_business.post_quiz_data(quiz_data, admin_id)
        return SuccessMessage(status=StatusCodes.CREATED, message=Message.QUIZ_POSTED).message_info

    @handle_custom_errors
    def update_question(self, question_id: str, question_data: str) -> None:
        '''Update question text by question id'''

        new_ques_text = question_data.get('question_text')
        self.question_business.update_question(question_id, new_ques_text)
        return SuccessMessage(status=StatusCodes.OK, message=Message.QUESTION_UPDATED).message_info

    @handle_custom_errors
    def delete_question(self, question_id: str) -> bool:
        '''Delete a question and its options by question id'''

        self.question_business.delete_question(question_id)
        return SuccessMessage(status=StatusCodes.OK, message=Message.QUESTION_DELETED).message_info

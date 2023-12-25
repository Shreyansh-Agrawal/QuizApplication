'''Helper functions for Starting Quiz'''

import logging
from datetime import datetime, timezone
from typing import List, Tuple

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage, Prompts
from config.queries import Queries
from config.regex_patterns import RegexPattern
from controllers.helpers.create_quiz_helper import CreateQuizHelper
from database.database_access import db
from utils import validations
from utils.custom_error import DataNotFoundError
from utils.pretty_print import pretty_print

logger = logging.getLogger(__name__)


class StartQuizHelper:
    '''StartQuizHelper containing methods for starting quiz for a player'''

    def get_random_questions(self) -> List[Tuple]:
        '''Return random questions across all categories'''

        data = db.read_from_database(Queries.GET_RANDOM_QUESTIONS)
        return data

    def get_random_questions_by_category(self, category: str) -> List[Tuple]:
        '''Return random questions by category'''

        data = db.read_from_database(Queries.GET_RANDOM_QUESTIONS_BY_CATEGORY, (category, ))
        return data

    def select_category(self) -> str:
        '''Takes in player input for category'''

        data = CreateQuizHelper().get_all_categories()
        if not data:
            raise DataNotFoundError(ErrorMessage.NO_CATEGORY_ERROR)

        categories = [(tup[0], ) for tup in data]
        pretty_print(data=categories, headers=(Headers.CATEGORY, ))

        player_choice = validations.regex_validator(
            prompt=Prompts.SELECT_CATEGORY_PROMPT,
            regex_pattern=RegexPattern.NUMERIC_PATTERN,
            error_msg=DisplayMessage.INVALID_CHOICE
        )
        player_choice = int(player_choice)
        if player_choice > len(categories) or player_choice-1 < 0:
            raise DataNotFoundError(DisplayMessage.CATEGORY_NOT_FOUND_MSG)

        category = categories[player_choice-1][0]
        return category

    def display_question(
        self, question_no: int, question: str, question_type: str, options_data: List[Tuple]
    ) -> None:
        '''Display question and its options to player'''

        print(f'\n{question_no}) {question}')
        if question_type.lower() == 'mcq':
            options = [option[0] for option in options_data]
            for count, option in enumerate(options, 1):
                print(f'    {count}. {option}')
        elif question_type.lower() == 't/f':
            print(DisplayMessage.TF_OPTION_MSG)

    def get_player_response(self, question_type: str) -> str:
        '''Gets player response according to question type'''

        if question_type.lower() == 'mcq':
            while True:
                player_choice = validations.regex_validator(
                    prompt=Prompts.SELECT_OPTION_PROMPT,
                    regex_pattern=RegexPattern.NUMERIC_PATTERN,
                    error_msg=DisplayMessage.INVALID_CHOICE
                )
                player_choice = int(player_choice)
                if player_choice not in range(1, 5):
                    print(DisplayMessage.MCQ_WRONG_OPTION_MSG)
                    continue
                return player_choice

        elif question_type.lower() == 't/f':
            while True:
                player_choice = validations.regex_validator(
                    prompt=Prompts.SELECT_OPTION_PROMPT,
                    regex_pattern=RegexPattern.NUMERIC_PATTERN,
                    error_msg=DisplayMessage.INVALID_CHOICE
                )
                player_choice = int(player_choice)
                match player_choice:
                    case 1:
                        return 'true'
                    case 2:
                        return 'false'
                    case _:
                        print(DisplayMessage.TF_WRONG_OPTION_MSG)
        else:
            player_answer = validations.regex_validator(
                prompt=Prompts.ANS_INPUT_PROMPT,
                regex_pattern=RegexPattern.OPTION_TEXT_PATTERN,
                error_msg=DisplayMessage.INVALID_TEXT.format(Headers.OPTION)
            )
            return player_answer

    def save_quiz_score(self, username: str, score: int) -> None:
        '''Save Player's Quiz Score'''

        logger.debug(LogMessage.SAVE_QUIZ_SCORE, username)
        player_data = db.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
        user_id = player_data[0][0]
        score_id = validations.validate_id(entity='score')

        time = datetime.now(timezone.utc) # current utc time
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # yyyy-mm-dd

        db.write_to_database(Queries.INSERT_PLAYER_QUIZ_SCORE, (score_id, user_id, score, timestamp))
        logger.debug(LogMessage.SAVE_QUIZ_SCORE_SUCCESS, username)

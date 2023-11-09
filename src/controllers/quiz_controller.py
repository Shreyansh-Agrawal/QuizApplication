'''Controllers for Operations related to Quiz'''

import logging
import sqlite3
import time
from typing import List, Tuple

from config.display_menu import DisplayMessage, Headers
from config.queries import Queries
from config.regex_patterns import RegexPattern
from controllers.helpers import quiz_helper as QuizHelper
from controllers.helpers import start_quiz_helper as StartQuizHelper
from database.database_access import DatabaseAccess as DAO
from models.quiz import Category
from utils import validations
from utils.custom_error import DataNotFoundError, DuplicateEntryError

logger = logging.getLogger(__name__)


def get_all_questions() -> List[Tuple]:
    '''Return all quiz questions'''

    data = DAO.read_from_database(Queries.GET_ALL_QUESTIONS_DETAIL)
    return data


def get_questions_by_category() -> List[Tuple]:
    '''Return quiz questions by category'''

    categories = QuizHelper.get_all_categories()

    logger.debug('Get Questions by Category')

    user_choice = validations.regex_validator(
        prompt='Choose a Category: ',
        regex_pattern=RegexPattern.NUMERIC_PATTERN,
        error_msg=DisplayMessage.INVALID_CHOICE
    )
    
    user_choice = int(user_choice)
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]

    print(DisplayMessage.DISPLAY_QUES_IN_A_CATEGORY_MSG.format(name=category_name))

    data = DAO.read_from_database(Queries.GET_QUESTIONS_BY_CATEGORY, (category_name, ))
    return data


def get_leaderboard() -> List[Tuple]:
    '''Return top 10 scores for leaderboard'''

    data = DAO.read_from_database(Queries.GET_LEADERBOARD)
    return data


def create_category(username: str) -> None:
    '''Add a Quiz Category'''

    admin_data = DAO.read_from_database(Queries.GET_USER_ID_BY_USERNAME, (username, ))
    admin_id = admin_data[0][0]

    logger.debug('Creating Category')
    print(DisplayMessage.CREATE_CATEGORY_MSG)

    category_data = {}
    category_data['admin_id'] = admin_id
    category_data['admin_username'] = username
    category_data['category_name'] = validations.regex_validator(
        prompt='Enter New Category Name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    ).title()

    category = Category(category_data)

    try:
        category.save_to_database()
    except sqlite3.IntegrityError as e:
        raise DuplicateEntryError('\nCategory already exists!') from e

    logger.debug('Category Created')
    print(DisplayMessage.CREATE_CATEGORY_SUCCESS_MSG)


def create_question(username: str) -> None:
    '''Add Questions in a Category'''

    question_data = QuizHelper.get_question_data(username)
    question = QuizHelper.create_option(question_data)

    try:
        question.save_to_database()
    except sqlite3.IntegrityError as e:
        raise DuplicateEntryError('Question already exists!') from e

    logger.debug('Question Created')
    print(DisplayMessage.CREATE_QUES_SUCCESS_MSG)


def update_category_by_name() -> None:
    '''Update a category by category name'''

    categories = QuizHelper.get_all_categories()

    logger.debug('Updating a Category')
    print(DisplayMessage.UPDATE_CATEGORY_MSG)

    user_choice = validations.regex_validator(
        prompt='Choose a Category: ',
        regex_pattern=RegexPattern.NUMERIC_PATTERN,
        error_msg=DisplayMessage.INVALID_CHOICE
    )

    user_choice = int(user_choice)
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]
    new_category_name = validations.regex_validator(
        prompt='Enter updated category name: ',
        regex_pattern=RegexPattern.NAME_PATTERN,
        error_msg=DisplayMessage.INVALID_TEXT.format(Headers.NAME)
    ).title()

    DAO.write_to_database(Queries.UPDATE_CATEGORY_BY_NAME, (new_category_name, category_name))

    logger.debug('Category %s updated to %s', category_name, new_category_name)
    print(DisplayMessage.UPDATE_CATEGORY_SUCCESS_MSG.format(name=category_name, new_name=new_category_name))


def delete_category_by_name() -> None:
    '''Delete a category by category name'''

    categories = QuizHelper.get_all_categories()

    logger.debug('Deleting a Category')
    print(DisplayMessage.DELETE_CATEGORY_MSG)

    user_choice = validations.regex_validator(
        prompt='Choose a Category: ',
        regex_pattern=RegexPattern.NUMERIC_PATTERN,
        error_msg=DisplayMessage.INVALID_CHOICE
    )

    user_choice = int(user_choice)
    if user_choice > len(categories) or user_choice-1 < 0:
        raise DataNotFoundError('No such Category! Please choose from above!!')

    category_name = categories[user_choice-1][0]

    while True:
        print(DisplayMessage.DELETE_CATEGORY_WARNING_MSG.format(name=category_name))
        confirmation = input('Type "YES" if you wish to continue\nPress any other key to go back: ')
        if confirmation.lower() == 'yes':
            break
        return

    logger.warning('Deleting the Category: %s', category_name)
    DAO.write_to_database(Queries.DELETE_CATEGORY_BY_NAME, (category_name, ))

    logger.debug('Category %s deleted', category_name)
    print(DisplayMessage.DELETE_CATEGORY_SUCCESS_MSG.format(name=category_name))


def start_quiz(username: str, category: str = None) -> None:
    '''Start a New Quiz'''

    logger.debug('Stating Quiz for: %s', username)
    if not category:
        data = StartQuizHelper.get_random_questions()
    else:
        data = StartQuizHelper.get_random_questions_by_category(category)

    if len(data) < 10:
        raise DataNotFoundError('Not enough questions!')

    end_time = time.time() + 5*60
    score = 0
    # Display question, take user's response and calculate score one by one
    for question_no, question_data in enumerate(data, 1):
        question_id, question_text, question_type, correct_answer = question_data
        options_data = DAO.read_from_database(Queries.GET_OPTIONS_FOR_MCQ, (question_id, ))

        remaining_time = end_time - time.time()
        if remaining_time <= 0:
            print('\nTime\'s up!')
            break

        mins = int(remaining_time//60)
        seconds = int(remaining_time % 60)
        print(f'\nTime remaining: {mins}:{seconds} mins')

        StartQuizHelper.display_question(question_no, question_text, question_type, options_data)

        user_answer = StartQuizHelper.get_user_response(question_type)

        if question_type.lower() == 'mcq':
            user_answer = options_data[user_answer-1][0]

        if user_answer.lower() == correct_answer.lower():
            score += 10

    print(DisplayMessage.DISPLAY_SCORE_MSG.format(score=score))
    StartQuizHelper.save_quiz_score(username, score)
    logger.debug('Quiz Completed for: %s', username)

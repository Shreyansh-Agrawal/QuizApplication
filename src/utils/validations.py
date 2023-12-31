'''Input Validations'''

import functools
import re

import maskpass
import shortuuid

from config.regex_patterns import RegexPattern
from config.message_prompts import DisplayMessage, Headers
from utils.custom_error import InvalidInputError


def error_handling(func):
    '''
    Decorator for error handling with regex validation.

    Args:
        func: The function to be decorated.

    This decorator adds error handling capabilities to functions that perform regex validation. It catches
    InvalidInputError exceptions raised during the function execution, prints an error message for the user,
    and returns False in case of an exception.

    Returns:
        wrapper: The decorated function.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except InvalidInputError as e:
            print(DisplayMessage.TRY_AGAIN_MSG.format(error=e))
            return False
        return res

    return wrapper


@error_handling
def validator(pattern: str, data: str, error_msg: str) -> bool:
    '''
    Validates input data based on a specified regex pattern.

    Args:
        pattern (str): The regex pattern against which the data will be validated.
        data (str): The data to be validated.
        error_msg (str): The error message to be displayed if validation fails.

    Raises:
        InvalidInputError: If the provided data does not match the specified pattern.

    Returns:
        bool: True if the data matches the pattern, else False.
    '''
    match_obj = re.fullmatch(pattern, data)
    if not match_obj:
        raise InvalidInputError(error_msg)

    return True


def validate_id(entity: str) -> str:
    '''
    Validates the ID generated by shortuuid.

    Args:
        entity (str): The entity for which the ID is generated.

    Returns:
        str: A validated ID for the specified entity.
    '''
    result = False
    prefix = entity[0].upper()
    regex_pattern = RegexPattern.ID_PATTERN

    while not result:
        entity_id = prefix + shortuuid.ShortUUID().random(length=5)
        result = validator(
            pattern=regex_pattern,
            data=entity_id,
            error_msg=DisplayMessage.INVALID_TEXT.format(Headers.ID)
        )

    return entity_id


def validate_password(prompt: str) -> str:
    '''
    Validates the password input from the user.

    Args:
        prompt (str): The prompt displayed to the user to input the password.

    Returns:
        str: A validated password input by the user.
    '''
    result = False
    password = ''
    regex_pattern = RegexPattern.PASSWORD_PATTERN

    while not result:
        password = maskpass.askpass(mask='*', prompt=prompt)
        result = validator(
            pattern=regex_pattern,
            data=password,
            error_msg=DisplayMessage.INVALID_PASSWORD
        )

    return password


def regex_validator(prompt: str, regex_pattern: str, error_msg: str) -> str:
    '''
    Validates user input based on a provided regex pattern.

    Args:
        prompt (str): The prompt displayed to the user to input data.
        regex_pattern (str): The regex pattern against which the user input will be validated.
        error_msg (str): The error message to be displayed if validation fails.

    Returns:
        str: The validated input data.
    '''
    result = False
    input_data = ''

    while not result:
        input_data = input(prompt).lower()
        result = validator(
            pattern=regex_pattern,
            data=input_data,
            error_msg=error_msg
        )

    return input_data

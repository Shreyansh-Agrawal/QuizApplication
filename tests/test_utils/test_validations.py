'''Test file for validations.py'''

import pytest
import shortuuid

from config.message_prompts import DisplayMessage, Headers
from config.regex_patterns import RegexPattern
from utils import validations

valid_validator_input_data = [
    (RegexPattern.NAME_PATTERN, 'John Doe', DisplayMessage.INVALID_TEXT.format(Headers.NAME)),
    (RegexPattern.EMAIL_PATTERN, 'shreyansh.agrawal@watchguard.com', DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)),
    (RegexPattern.USERNAME_PATTERN, 'shreyansh.agr_07', DisplayMessage.INVALID_TEXT.format(Headers.USERNAME)),
    (RegexPattern.QUES_TEXT_PATTERN, 'What is 1+1 ?', DisplayMessage.INVALID_TEXT.format(Headers.QUES)),
    (RegexPattern.OPTION_TEXT_PATTERN, 'Option 1', DisplayMessage.INVALID_TEXT.format(Headers.OPTION)),
    (RegexPattern.NUMERIC_PATTERN, '12', DisplayMessage.INVALID_TEXT.format(Headers.CATEGORY)),
    (RegexPattern.PASSWORD_PATTERN, '123456', DisplayMessage.INVALID_TEXT.format(Headers.PASSWORD)),
    (RegexPattern.ID_PATTERN, 'SXGLul', DisplayMessage.INVALID_TEXT.format(Headers.ID))
]

invalid_validator_input_data = [
    (RegexPattern.NAME_PATTERN, '$hreyansh', DisplayMessage.INVALID_TEXT.format(Headers.NAME)),
    (RegexPattern.EMAIL_PATTERN, 'some.email.com', DisplayMessage.INVALID_TEXT.format(Headers.EMAIL)),
    (RegexPattern.USERNAME_PATTERN, 'shreyansh@agr', DisplayMessage.INVALID_TEXT.format(Headers.USERNAME)),
    (RegexPattern.QUES_TEXT_PATTERN, 'Too short', DisplayMessage.INVALID_TEXT.format(Headers.QUES)),
    (RegexPattern.OPTION_TEXT_PATTERN, '', DisplayMessage.INVALID_TEXT.format(Headers.OPTION)),
    (RegexPattern.NUMERIC_PATTERN, '!2', DisplayMessage.INVALID_TEXT.format(Headers.CATEGORY)),
    (RegexPattern.PASSWORD_PATTERN, '12345', DisplayMessage.INVALID_TEXT.format(Headers.PASSWORD)),
    (RegexPattern.ID_PATTERN, 'SXG1ul', DisplayMessage.INVALID_TEXT.format(Headers.ID))
]

entity_data = ['SuperAdmin', 'Admin', 'Player', 'User']


@pytest.mark.parametrize('pattern, data, error_msg', valid_validator_input_data)
def test_validator_valid_input(pattern: str, data: str, error_msg: str):
    '''Test function to test validator for correct data'''

    assert validations.validator(pattern, data, error_msg)


@pytest.mark.parametrize('pattern, data, error_msg', invalid_validator_input_data)
def test_validator_invalid_input(pattern: str, data: str, error_msg: str):
    '''Test function to test validator for incorrect data'''

    assert not validations.validator(pattern, data, error_msg)


@pytest.mark.parametrize('entity', entity_data)
def test_validate_id(entity: str):
    '''Test function to test valid_id function'''

    prefix = entity[0].upper()
    generated_id = validations.validate_id(entity)

    assert generated_id.startswith(prefix)
    assert len(generated_id) == len(prefix+shortuuid.ShortUUID().random(length=5))


def test_validate_password(monkeypatch):
    '''Test function to test valid_id function'''

    test_password = 'Test123456'
    monkeypatch.setattr('maskpass.askpass', lambda **kwargs: test_password)
    password = validations.validate_password('prompt')

    assert password == test_password
    assert len(password) >= 6


@pytest.mark.parametrize('pattern, test_data, error_msg', valid_validator_input_data)
def test_regex_validator(pattern: str, test_data: str, error_msg: str, monkeypatch):
    '''Test function to test regex validator function'''

    monkeypatch.setattr('builtins.input', lambda _ : test_data)
    input_data = validations.regex_validator('prompt', pattern, error_msg)
    assert test_data.lower() == input_data

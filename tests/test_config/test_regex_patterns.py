'''Test file for regex_patterns.py'''

import re

from src.config.regex_patterns import RegexPattern


def test_name_pattern():
    '''Test function to test NAME_PATTERN regex'''

    assert re.fullmatch(RegexPattern.NAME_PATTERN, 'John Doe')
    assert not re.fullmatch(RegexPattern.NAME_PATTERN, 'J0hnD03')  # Check for invalid characters


def test_email_pattern():
    '''Test function to test EMAIL_PATTERN regex'''

    assert re.fullmatch(RegexPattern.EMAIL_PATTERN, 'example@example.com')
    assert not re.fullmatch(RegexPattern.EMAIL_PATTERN, 'example@.com')  # Check for invalid format


def test_username_pattern():
    '''Test function to test USERNAME_PATTERN regex'''

    assert re.fullmatch(RegexPattern.USERNAME_PATTERN, 'user_name_123')
    assert not re.fullmatch(RegexPattern.USERNAME_PATTERN, 'user$123')  # Check for invalid characters


def test_ques_text_pattern():
    '''Test function to test QUES_TEXT_PATTERN regex'''

    assert re.fullmatch(RegexPattern.QUES_TEXT_PATTERN, 'This is a valid question text.')
    assert not re.fullmatch(RegexPattern.QUES_TEXT_PATTERN, 'Short')  # Check for text length


def test_option_text_pattern():
    '''Test function to test OPTION_TEXT_PATTERN regex'''

    assert re.fullmatch(RegexPattern.OPTION_TEXT_PATTERN, 'Valid option text.')
    assert not re.fullmatch(
        RegexPattern.OPTION_TEXT_PATTERN,
        'This is a very long option text that exceeds the limit allowed.'
    )  # Check for text length


def test_numeric_pattern():
    '''Test function to test NUMERIC_PATTERN regex'''

    assert re.fullmatch(RegexPattern.NUMERIC_PATTERN, '123456')
    assert not re.fullmatch(RegexPattern.NUMERIC_PATTERN, '12ab34')  # Check for non-numeric characters


def test_password_pattern():
    '''Test function to test PASSWORD_PATTERN regex'''

    assert re.fullmatch(RegexPattern.PASSWORD_PATTERN, 'securePwd123')
    assert not re.fullmatch(RegexPattern.PASSWORD_PATTERN, 'short')  # Check for minimum length


def test_id_pattern():
    '''Test function to test ID_PATTERN regex'''

    assert re.fullmatch(RegexPattern.ID_PATTERN, 'aB2345')
    assert not re.fullmatch(RegexPattern.ID_PATTERN, 'invalidID@#')  # Check for invalid characters

'''Contains regex patterns for validating various inputs'''

class RegexPattern:
    '''Contains regex patterns as class variables'''

    NAME_PATTERN = r'[A-Za-z\s]{2,25}'
    EMAIL_PATTERN = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}'
    USERNAME_PATTERN = r'[A-Za-z0-9._]{2,30}'
    QUES_TEXT_PATTERN = r'.{10,100}'
    OPTION_TEXT_PATTERN = r'.{1,50}'
    NUMERIC_PATTERN = r'^[0-9]+'
    PASSWORD_PATTERN = r'.{6,}'
    ID_PATTERN = r'[a-zA-z2-9]{6}'

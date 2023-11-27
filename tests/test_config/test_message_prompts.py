'''Test file for message_prompts.py'''


def test_display_message_attributes(display_message_attributes):
    '''Test if DisplayMessage class has all required messages defined'''

    required_messages = [
        'APP_WELCOME_MSG',
        'EXIT_MSG',
        'AUTH_INVALIDATE_MSG',
        'CONFIRM_PSWD_FAIL_MSG',
        'LOGIN_SUCCESS_MSG',
        'SIGNUP_SUCCESS_MSG',
        'DISPLAY_QUES_IN_A_CATEGORY_MSG',
        'CREATE_CATEGORY_MSG',
        'CREATE_CATEGORY_SUCCESS_MSG',
        'CREATE_QUES_MSG',
        'CREATE_QUES_SUCCESS_MSG',
        'INVALID_QUES_TYPE_MSG',
        'UPDATE_CATEGORY_MSG',
        'UPDATE_CATEGORY_SUCCESS_MSG',
        'DELETE_CATEGORY_MSG',
        'DELETE_CATEGORY_WARNING_MSG',
        'DELETE_CATEGORY_SUCCESS_MSG',
        'DISPLAY_SCORE_MSG',
        'TF_OPTION_MSG',
        'MCQ_WRONG_OPTION_MSG',
        'TF_WRONG_OPTION_MSG',
        'CREATE_ADMIN_MSG',
        'CREATE_ADMIN_SUCCESS_MSG',
        'DELETE_USER_MSG',
        'DELETE_USER_FAIL_MSG',
        'DELETE_USER_SUCCESS_MSG',
        'LOGIN_MSG',
        'REMAINING_ATTEMPTS_MSG',
        'LOGIN_ATTEMPTS_EXHAUST_MSG',
        'SIGNUP_MSG',
        'REDIRECT_MSG',
        'CHANGE_PSWD_MSG',
        'CHANGE_PSWD_SUCCESS_MSG',
        'WRONG_INPUT_MSG',
        'LOAD_QUES_MSG',
        'MANAGE_CATEGORIES_MSG',
        'MANAGE_QUES_MSG',
        'CATEGORIES_MSG',
        'QUES_NOT_FOUND_MSG',
        'QUES_MSG',
        'QUIZ_DATA_NOT_FOUND_MSG',
        'LEADERBOARD_MSG',
        'QUIZ_START_MSG',
        'CATEGORY_NOT_FOUND_MSG',
        'USER_NOT_FOUND_MSG',
        'DISPLAY_USERS_MSG',
        'SCORE_DATA_MSG',
        'HIGHEST_SCORE_MSG',
        'CREATE_SUPER_ADMIN_SUCCESS_MSG',
        'INITIALIZATION_SUCCESS_MSG',
        'USER_WELCOME_MSG',
        'MANAGE_PLAYERS_MSG',
        'MANAGE_QUIZ_MSG',
        'DASHBOARD_MSG',
        'INVALID_ROLE_MSG',
        'TABULATE_ERROR_MSG',
        'TRY_AGAIN_MSG',
        'INVALID_TEXT',
        'INVALID_CHOICE',
        'INVALID_PASSWORD'
    ]

    for message in required_messages:
        assert message in display_message_attributes


def test_prompts_attributes(prompts_attributes):
    '''Test if Prompts class has all required prompts defined'''

    required_prompts = [
        'AUTH_PROMPTS',
        'SUPER_ADMIN_PROMPTS',
        'ADMIN_PROMPTS',
        'ADMIN_MANAGE_PLAYER_PROMPTS',
        'ADMIN_MANAGE_QUIZZES_PROMPTS',
        'ADMIN_MANAGE_CATEGORIES_PROMPTS',
        'ADMIN_MANAGE_QUESTIONS_PROMPTS',
        'PLAYER_PROMPTS',
        'QUESTION_TYPE_PROMPTS',
        'SELECT_MODE_PROMPTS',
        'ATTEMPT_LIMIT'
    ]

    for prompt in required_prompts:
        assert prompt in prompts_attributes


def test_headers_attributes(headers_attributes):
    '''Test if Headers class has all required headers defined'''

    required_headers = [
        'USERNAME',
        'NAME',
        'EMAIL',
        'PASSWORD',
        'REG_DATE',
        'CATEGORY',
        'QUES',
        'QUES_TYPE',
        'ANS',
        'CREATED_BY',
        'SCORE',
        'TIME',
        'ID',
        'OPTION',
        'PLAYER_ANS',
        'SUPER_ADMIN',
        'ADMIN',
        'PLAYER',
        'QUIZZES'
    ]

    for header in required_headers:
        assert header in headers_attributes


def test_log_message_attributes(log_message_attributes):
    '''Test if LogMessage class has all required log messages defined'''

    required_log_messages = [
        'LOGIN_INITIATED',
        'LOGIN_SUCCESS',
        'SIGNUP_INITIATED',
        'SIGNUP_SUCCESS',
        'SYSTEM_START',
        'SYSTEM_STOP',
        'INITIALIZE_APP_SUCCESS',
        'CREATE_ENTITY',
        'CREATE_SUCCESS',
        'UPDATE_ENTITY',
        'UPDATE_SUCCESS',
        'DELETE_ENTITY',
        'DELETE_SUCCESS',
        'DELETE_CATEGORY',
        'DELETE_CATEGORY_SUCCESS',
        'CHANGE_DEFAULT_ADMIN_PSW',
        'CHANGE_DEFAULT_ADMIN_PSW_SUCCESS',
        'UPDATE_CATEGORY_SUCCESS',
        'GET_QUES_BY_CATEGORY',
        'START_QUIZ',
        'COMPLETE_QUIZ',
        'RUNNING_USER_MENU',
        'RUNNING_AUTH_MENU',
        'ASSIGN_MENU',
        'SUPER_ADMIN_PRESENT',
        'TABULATE_ERROR',
        'SAVE_QUIZ_SCORE',
        'SAVE_QUIZ_SCORE_SUCCESS',
        'DISPLAY_QUIZ_SCORE',
        'DISPLAY_ALL_ENTITY',
        'DISPLAY_QUES_BY_CATEGORY',
        'INVALID_QUES_TYPE',
        'LOGIN_ATTEMPTS_EXHAUSTED',
        'LEADERBOARD_DATA_NOT_FOUND',
        'QUES_DATA_NOT_FOUND',
        'RUNNING_ADMIN_MENU',
        'LOAD_QUIZ_DATA_FROM_JSON'
    ]

    for log_message in required_log_messages:
        assert log_message in log_message_attributes

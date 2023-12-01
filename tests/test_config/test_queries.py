'''Test file for queries.py'''


def test_initialization_queries(initialization_queries_attributes):
    '''Test InitializationQueries to check if the queries are not empty'''

    required_queries = [
        'CREATE_CATEGORIES_TABLE',
        'CREATE_CREDENTIALS_TABLE',
        'CREATE_OPTIONS_TABLE',
        'CREATE_QUESTIONS_TABLE',
        'CREATE_SCORES_TABLE',
        'CREATE_USERS_TABLE',
        'ENABLE_FOREIGN_KEYS'
    ]

    for query in required_queries:
        assert query in initialization_queries_attributes


def test_queries(queries_attributes):
    '''Test Queries to check if the queries are not empty'''

    required_queries = [
        'INSERT_CATEGORY',
        'INSERT_CREDENTIALS',
        'INSERT_OPTION',
        'INSERT_QUESTION',
        'INSERT_USER_DATA',
        'INSERT_PLAYER_QUIZ_SCORE',
        'GET_ALL_CATEGORIES',
        'GET_ALL_QUESTIONS_DETAIL',
        'GET_CATEGORY_ID_BY_NAME',
        'GET_CREDENTIALS_BY_USERNAME',
        'GET_LEADERBOARD',
        'GET_OPTIONS_FOR_MCQ',
        'GET_QUESTIONS_BY_CATEGORY',
        'GET_RANDOM_QUESTIONS',
        'GET_RANDOM_QUESTIONS_BY_CATEGORY',
        'GET_USER_BY_ROLE',
        'GET_USER_BY_USERNAME',
        'GET_USER_ID_BY_USERNAME',
        'GET_PLAYER_SCORES_BY_USERNAME',
        'UPDATE_ADMIN_PASSWORD_BY_USERNAME',
        'UPDATE_CATEGORY_BY_NAME',
        'UPDATE_QUESTION_TEXT_BY_ID',
        'DELETE_CATEGORY_BY_NAME',
        'DELETE_QUESTION_BY_ID',
        'DELETE_USER_BY_EMAIL'
    ]

    for query in required_queries:
        assert query in queries_attributes

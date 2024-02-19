'''Contains all the pytest fixtures'''

import pytest

from config.string_constants import Headers, LogMessage, ErrorMessage
from config.queries import InitializationQueries, Queries


@pytest.fixture
def user_data():
    '''Test Fixture to return test data for any user'''

    return {
        'name': 'Test User',
        'email': 'test@email.com',
        'username': 'test_username',
        'password': 'Test@123'
    }


@pytest.fixture
def category_data():
    '''Test Fixture to return category data'''

    return {
        'category_name': 'Science',
        'admin_id': 123,
        'admin_username': 'admin123'
    }


@pytest.fixture
def question_data():
    '''Test Fixture to return question data'''

    return {
        'question_text': 'What is 2 + 2?',
        'category_id': 123,
        'admin_id': 456,
        'admin_username': 'admin',
        'question_type': 'MCQ'
    }


@pytest.fixture
def option_data():
    '''Test Fixture to return option data'''

    return {
        'option_text': 'Option A',
        'question_id': 123,
        'is_correct': 1
    }


@pytest.fixture
def mock_user(mocker):
    '''Test Fixture to mock user details'''

    user = mocker.Mock()
    user.configure_mock(
        user_id=1,
        name='John Doe',
        email='john@example.com',
        role='user',
        registration_date='2023-11-28',
        username='johndoe',
        password='pass123',
        is_password_changed=1
    )
    return user


@pytest.fixture
def mock_env_variables(monkeypatch, user_data):
    '''Test Fixture to mock the environment variables'''

    monkeypatch.setenv('SUPER_ADMIN_NAME', user_data['name'])
    monkeypatch.setenv('SUPER_ADMIN_EMAIL', user_data['email'])
    monkeypatch.setenv('SUPER_ADMIN_USERNAME', user_data['username'])
    monkeypatch.setenv('SUPER_ADMIN_PASSWORD', user_data['password'])


@pytest.fixture
def headers_attributes():
    '''Test Fixture to collect and returns attributes from the Headers class.'''

    return [attr for attr in dir(Headers) if not attr.startswith('__')]


@pytest.fixture
def prompts_attributes():
    '''Test Fixture to collect and returns attributes from the Prompts class.'''

    return [attr for attr in dir(Prompts) if not attr.startswith('__')]


@pytest.fixture
def display_message_attributes():
    '''Test Fixture to collect and returns attributes from the DisplayMessage class.'''

    return [attr for attr in dir(DisplayMessage) if not attr.startswith('__')]


@pytest.fixture
def initialization_queries_attributes():
    '''Test Fixture to collect and returns attributes from the InitializationQueries class.'''

    return [attr for attr in dir(InitializationQueries) if not attr.startswith('__')]


@pytest.fixture
def queries_attributes():
    '''Test Fixture to collect and returns attributes from the Queries class.'''

    return [attr for attr in dir(Queries) if not attr.startswith('__')]


@pytest.fixture
def log_message_attributes():
    '''Test Fixture to collect and returns attributes from the LogMessage class.'''

    return [attr for attr in dir(LogMessage) if not attr.startswith('__')]


@pytest.fixture
def file_paths_attributes():
    '''Test Fixture to collect and returns attributes from the FilePaths class.'''

    return [attr for attr in dir(FilePaths) if not attr.startswith('__')]


@pytest.fixture
def error_message_attributes():
    '''Test Fixture to collect and returns attributes from the ErrorMessage class.'''

    return [attr for attr in dir(ErrorMessage) if not attr.startswith('__')]


@pytest.fixture
def sample_json_data():
    '''Test Fixture to mock json data'''

    return {
        "questions": [
            {
                "question_id": "Q001",
                "question_text": "What is the chemical symbol for water?",
                "question_type": "one-word",
                "category_id": "C002",
                "category": "Science",
                "admin_id": "A002",
                "admin_username": "sciencenerd",
                "options": {
                    "answer": {"option_id": "A001", "text": "H2O"},
                    "other_options": [],
                },
            },
            {
                "question_id": "Q002",
                "question_text": "Which gas is responsible for the Earth's greenhouse effect?",
                "question_type": "mcq",
                "category_id": "C002",
                "category": "Science",
                "admin_id": "A002",
                "admin_username": "sciencenerd",
                "options": {
                    "answer": {"option_id": "A102", "text": "Carbon dioxide"},
                    "other_options": [
                        {"option_id": "A103", "text": "Oxygen"},
                        {"option_id": "A004", "text": "Nitrogen"},
                        {"option_id": "A005", "text": "Methane"},
                    ],
                },
            },
        ]
    }

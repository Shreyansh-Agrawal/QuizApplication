'''Contains all the pytest fixtures'''

import sqlite3

import pytest

from src.config.file_paths import FilePaths
from src.config.message_prompts import DisplayMessage, Headers, LogMessage, Prompts
from src.config.queries import InitializationQueries, Queries
from src.utils.custom_error import DuplicateEntryError


@pytest.fixture
def mock_env_variables(monkeypatch):
    '''Test Fixture to mock the environment variables'''

    monkeypatch.setenv('SUPER_ADMIN_NAME', 'Super Admin')
    monkeypatch.setenv('SUPER_ADMIN_EMAIL', 'test@email.com')
    monkeypatch.setenv('SUPER_ADMIN_USERNAME', 'test_username')
    monkeypatch.setenv('SUPER_ADMIN_PASSWORD', 'Test@123')


@pytest.fixture
def mock_super_admin(mocker):
    '''Test Fixture to Mock the SuperAdmin class'''

    mock_super_admin_class = mocker.Mock()
    mocker.patch('src.utils.initialize_app.SuperAdmin', mock_super_admin_class)
    mock_super_admin_class().save_to_database.return_value = None


@pytest.fixture
def mock_super_admin_duplicate(mocker):
    '''Test Fixture to Mock the SuperAdmin class to raise DuplicateEntry Error'''

    mock_super_admin_class = mocker.Mock()
    mocker.patch('src.utils.initialize_app.SuperAdmin', mock_super_admin_class)
    mock_super_admin_class().save_to_database.side_effect = DuplicateEntryError('Super Admin Already exists!')


@pytest.fixture
def mock_initialize_app(mocker):
    '''Test Fixture to Mock the initialize_app function'''

    mock_initialize_database_class = mocker.Mock()
    mock_initializer_class = mocker.Mock()
    mocker.patch('src.utils.initialize_app.InitializeDatabase', mock_initialize_database_class)
    mocker.patch('src.utils.initialize_app.Initializer', mock_initializer_class)


@pytest.fixture
def headers_attributes():
    '''Test Fixture to collect and returns attributes from the Headers class.'''

    return [attr for attr in dir(Headers) if not attr.startswith("__")]


@pytest.fixture
def prompts_attributes():
    '''Test Fixture to collect and returns attributes from the Prompts class.'''

    return [attr for attr in dir(Prompts) if not attr.startswith("__")]


@pytest.fixture
def display_message_attributes():
    '''Test Fixture to collect and returns attributes from the DisplayMessage class.'''

    return [attr for attr in dir(DisplayMessage) if not attr.startswith("__")]


@pytest.fixture
def initialization_queries_attributes():
    '''Test Fixture to collect and returns attributes from the InitializationQueries class.'''

    return [attr for attr in dir(InitializationQueries) if not attr.startswith("__")]


@pytest.fixture
def queries_attributes():
    '''Test Fixture to collect and returns attributes from the Queries class.'''

    return [attr for attr in dir(Queries) if not attr.startswith("__")]


@pytest.fixture
def log_message_attributes():
    '''Test Fixture to collect and returns attributes from the LogMessage class.'''

    return [attr for attr in dir(LogMessage) if not attr.startswith("__")]


@pytest.fixture
def file_paths_attributes():
    '''Test Fixture to collect and returns attributes from the FilePaths class.'''

    return [attr for attr in dir(FilePaths) if not attr.startswith("__")]


@pytest.fixture
def mock_read_from_database_valid_data():
    '''Test Fixture to mock read_from_database method with valid data.'''

    def func_with_data():
        return [("John", "Doe"), ("Peter", "Pan")]

    return func_with_data


@pytest.fixture
def mock_read_from_database_no_data():
    '''Test Fixture to mock read_from_database method with no data.'''

    def func_with_no_data():
        return []

    return func_with_no_data


@pytest.fixture
def mock_read_from_database_with_error():
    '''Test Fixture to mock read_from_database method.'''

    def func_with_error():
        raise sqlite3.Error

    return func_with_error


@pytest.fixture
def mock_write_to_database():
    '''Test Fixture to mock write_to_database method.'''

    def func_with_no_error():
        pass

    return func_with_no_error


@pytest.fixture
def mock_write_to_database_with_error():
    '''Test Fixture to mock write_to_database method with error.'''

    def func_with_error():
        raise sqlite3.Error

    return func_with_error


@pytest.fixture
def sample_json_data():
    '''Test Fixture to mock json data'''

    return {
        "questions": [
            {
                "question_id": "Q001",
                "question_text": "What is the chemical symbol for water?",
                "question_type": "one word",
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
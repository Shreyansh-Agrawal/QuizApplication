'''Test file for initialize_app.py'''

import pytest

from src.config.message_prompts import DisplayMessage, Headers, LogMessage
from src.utils.custom_error import DuplicateEntryError
from src.utils.initialize_app import InitializeDatabase, Initializer


@pytest.mark.usefixtures('mock_env_variables', 'mock_super_admin')
def test_create_super_admin_success(capsys, caplog):
    '''Test function to test create_super_admin method success'''

    Initializer.create_super_admin()
    captured = capsys.readouterr()

    assert LogMessage.CREATE_SUCCESS, Headers.SUPER_ADMIN in caplog.text
    assert DisplayMessage.CREATE_SUPER_ADMIN_SUCCESS_MSG in captured.out


@pytest.mark.usefixtures('mock_super_admin_duplicate')
def test_create_super_admin_failure():
    '''Test function to test create_super_admin method failure'''

    with pytest.raises(DuplicateEntryError):
        Initializer.create_super_admin()


@pytest.mark.usefixtures('mock_initialize_app')
def test_initialize_app(capsys, caplog):
    '''Test function to test initialize_app method'''

    Initializer.initialize_app()
    captured = capsys.readouterr()

    assert LogMessage.INITIALIZE_APP_SUCCESS in caplog.text
    assert DisplayMessage.INITIALIZATION_SUCCESS_MSG in captured.out


def test_initialize_database(mocker):
    '''Test function to test initialize_database method'''

    mock_write_to_database = mocker.Mock()
    mocker.patch('src.utils.initialize_app.DAO.write_to_database', mock_write_to_database)

    InitializeDatabase.initialize_database()
    assert mock_write_to_database.call_count == 6

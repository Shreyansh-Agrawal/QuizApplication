'''Test file for initialize_app.py'''

import pytest

from src.config.message_prompts import DisplayMessage, Headers, LogMessage
from src.utils.custom_error import DuplicateEntryError
from src.utils.initialize_app import InitializeDatabase, Initializer


@pytest.mark.usefixtures('mock_env_variables')
def test_create_super_admin_success(mocker, capsys, caplog, user_data):
    '''Test function to test create_super_admin method success'''

    mocker.patch('src.utils.initialize_app.hash_password', return_value = user_data['password'])
    mock_super_admin = mocker.patch('src.utils.initialize_app.SuperAdmin')
    Initializer.create_super_admin()
    captured = capsys.readouterr()

    mock_super_admin.assert_called_once_with(user_data)
    mock_super_admin().save_to_database.assert_called_once()
    assert LogMessage.CREATE_SUCCESS, Headers.SUPER_ADMIN in caplog.text
    assert DisplayMessage.CREATE_SUPER_ADMIN_SUCCESS_MSG in captured.out


@pytest.mark.usefixtures('mock_env_variables')
def test_create_super_admin_failure(mocker):
    '''Test function to test create_super_admin method failure'''

    mock_super_admin = mocker.patch('src.utils.initialize_app.SuperAdmin')
    mock_super_admin().save_to_database.side_effect = DuplicateEntryError('Super Admin Already exists!')

    with pytest.raises(DuplicateEntryError):
        Initializer.create_super_admin()


def test_initialize_app(mocker, capsys, caplog):
    '''Test function to test initialize_app method'''

    mocker.patch('src.utils.initialize_app.InitializeDatabase')
    mocker.patch('src.utils.initialize_app.Initializer')
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

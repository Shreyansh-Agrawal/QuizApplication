'''Test file for auth_handler.py'''

import pytest
from config.message_prompts import DisplayMessage, LogMessage
from helpers.auth_handler import AuthHandler
from utils.custom_error import LoginError


class TestAuthHandler:
    '''Test class containing test methods for Auth Handler class'''

    username = 'test_username'
    password = 'test_password'
    wrong_password = 'test_wrong_password'
    name = 'test_name'
    email = 'test@email.com'
    error_msg = 'Login error'
    auth_handler = AuthHandler()
    mock_data = [('mock_data'), ('for_successful_login')]

    @pytest.fixture
    def mock_auth_controller_class(self, mocker):
        '''Test fixture to mock Authentication class'''

        return mocker.patch('controllers.handlers.auth_handler.Authentication')

    def test_handle_login_success(self, mocker, capsys, caplog, mock_auth_controller_class):
        '''Test method to test handle login for successful login'''

        mocker.patch('controllers.handlers.auth_handler.validations.regex_validator', return_value = self.username)
        mocker.patch('controllers.handlers.auth_handler.validations.validate_password', return_value = self.password)
        auth_controller = mock_auth_controller_class()
        auth_controller.login.return_value = self.mock_data
        self.auth_handler.auth_controller = auth_controller

        result = self.auth_handler.handle_login()
        captured = capsys.readouterr()

        assert DisplayMessage.LOGIN_MSG in captured.out
        assert LogMessage.LOGIN_SUCCESS in caplog.text
        assert result == self.mock_data

    def test_handle_login_failure(self, mocker, caplog, capsys, mock_auth_controller_class):
        '''Test method to test handle login for unsuccessful login'''

        mocker.patch('controllers.handlers.auth_handler.validations.regex_validator', return_value = self.username)
        mocker.patch('controllers.handlers.auth_handler.validations.validate_password', return_value = self.password)
        auth_controller = mock_auth_controller_class()
        auth_controller.login.return_value = None
        self.auth_handler.auth_controller = auth_controller

        result = self.auth_handler.handle_login()
        captured = capsys.readouterr()

        assert DisplayMessage.LOGIN_ATTEMPTS_EXHAUST_MSG in captured.out
        assert LogMessage.LOGIN_ATTEMPTS_EXHAUSTED in caplog.text
        assert not result

    def test_handle_signup_success(self, mocker, caplog, capsys, mock_auth_controller_class):
        '''Test method to test handle signup for successful signup'''

        mocker.patch('controllers.handlers.auth_handler.validations.regex_validator', side_effect = [self.name, self.email, self.username])
        mocker.patch('controllers.handlers.auth_handler.validations.validate_password', return_value = self.password)
        auth_controller = mock_auth_controller_class()
        auth_controller.signup.return_value = self.username
        self.auth_handler.auth_controller = auth_controller

        result = self.auth_handler.handle_signup()
        captured = capsys.readouterr()

        assert DisplayMessage.SIGNUP_MSG in captured.out
        assert DisplayMessage.REDIRECT_MSG in captured.out
        assert LogMessage.SIGNUP_INITIATED in caplog.text
        assert LogMessage.SIGNUP_SUCCESS in caplog.text
        assert result == self.username

    def test_handle_signup_failure(self, mocker, caplog, capsys, mock_auth_controller_class):
        '''Test method to test handle signup for unsuccessful signup'''

        mocker.patch('controllers.handlers.auth_handler.validations.regex_validator', side_effect = [self.name, self.email, self.username])
        mocker.patch('controllers.handlers.auth_handler.validations.validate_password', side_effect = [self.password, self.wrong_password, self.password])
        auth_controller = mock_auth_controller_class()
        auth_controller.signup.side_effect = LoginError(self.error_msg)
        self.auth_handler.auth_controller = auth_controller

        result = self.auth_handler.handle_signup()
        captured = capsys.readouterr()

        assert self.error_msg in captured.out
        assert self.error_msg in caplog.text
        assert not result

    def test_handle_first_login(self, mocker, caplog, capsys):
        '''Test method to test handle first login'''

        mocker.patch('controllers.handlers.auth_handler.validations.validate_password', side_effect = [self.password, self.wrong_password, self.password])
        mocker.patch('controllers.handlers.auth_handler.hash_password', return_value = 'hashed_password')
        mock_write = mocker.patch('controllers.handlers.auth_handler.db.write')

        self.auth_handler.handle_first_login(self.username, 0)
        captured = capsys.readouterr()

        assert DisplayMessage.CHANGE_PSWD_MSG in captured.out
        assert DisplayMessage.CHANGE_PSWD_SUCCESS_MSG in captured.out
        assert LogMessage.CHANGE_DEFAULT_ADMIN_PSW in caplog.text
        assert LogMessage.CHANGE_DEFAULT_ADMIN_PSW_SUCCESS in caplog.text
        mock_write.assert_called_once()

'''Test file for user_handler.py'''

import pytest

from config.message_prompts import DisplayMessage, Headers, LogMessage
from helpers.user_handler import UserHandler
from utils.custom_error import LoginError


class TestUserHandler:
    '''Test class containing test methods for User Handler class'''

    username = 'test_username'
    role = 'player'
    name = 'test name'
    email = 'test@email.com'
    header = ('header', )
    mock_data = [('test_user', 'test_name', 'test@email.com', 'player')]
    mock_invalid_data = [('test_user', 'test_name', 'test1@email.com', 'player')]
    error_msg = 'test error msg'
    user_handler = UserHandler()

    @pytest.fixture(autouse=True)
    def mock_pretty_print(self, mocker):
        '''Test fixture to mock pretty print'''

        return mocker.patch('controllers.handlers.user_handler.pretty_print')

    @pytest.fixture
    def mock_user_controller_class(self, mocker):
        '''Test fixture to mock UserController class'''

        return mocker.patch('controllers.handlers.user_handler.UserController')

    def test_display_users_by_role(self, capsys, caplog, mock_user_controller_class):
        '''Test method to test display_users_by_role'''

        user_controller = mock_user_controller_class()
        user_controller.get_all_users_by_role.return_value = self.mock_data
        self.user_handler.user_controller = user_controller

        self.user_handler.display_users_by_role(self.role)
        captured = capsys.readouterr()

        assert LogMessage.DISPLAY_ALL_ENTITY, self.role in caplog.text
        assert DisplayMessage.DISPLAY_USERS_MSG.format(user=self.role.title()) in captured.out

    def test_display_users_by_role_no_user(self, capsys, mock_user_controller_class):
        '''Test method to test display_users_by_role when no user present'''

        user_controller = mock_user_controller_class()
        user_controller.get_all_users_by_role.return_value = None
        self.user_handler.user_controller = user_controller

        self.user_handler.display_users_by_role(self.role)
        captured = capsys.readouterr()

        assert DisplayMessage.USER_NOT_FOUND_MSG.format(user=self.role) in captured.out

    def test_display_player_score(self, capsys, caplog, mock_user_controller_class):
        '''Test method to test display_player_score'''

        user_controller = mock_user_controller_class()
        user_controller.get_player_scores_by_username.return_value = self.mock_data
        self.user_handler.user_controller = user_controller

        self.user_handler.display_player_score(self.role)
        captured = capsys.readouterr()

        assert LogMessage.DISPLAY_QUIZ_SCORE, self.username in caplog.text
        assert DisplayMessage.SCORE_DATA_MSG in captured.out

    def test_display_player_score_no_data(self, capsys, mock_user_controller_class):
        '''Test method to test display_player_score when no data'''

        user_controller = mock_user_controller_class()
        user_controller.get_player_scores_by_username.return_value = None
        self.user_handler.user_controller = user_controller

        self.user_handler.display_player_score(self.role)
        captured = capsys.readouterr()

        assert DisplayMessage.QUIZ_DATA_NOT_FOUND_MSG in captured.out

    def test_handle_create_admin(self, mocker, capsys, caplog, mock_user_controller_class):
        '''Test method to test handle_create_admin with login error'''

        mocker.patch('controllers.handlers.user_handler.validations.regex_validator', side_effect=[self.name, self.email, self.username])
        user_controller = mock_user_controller_class()
        user_controller.create_admin.side_effect = LoginError(self.error_msg)
        self.user_handler.user_controller = user_controller

        self.user_handler.handle_create_admin()
        captured = capsys.readouterr()

        assert LogMessage.CREATE_ENTITY, Headers.ADMIN in caplog.text
        assert self.error_msg in caplog.text
        assert DisplayMessage.CREATE_ADMIN_MSG in captured.out
        assert self.error_msg in captured.out
        self.user_handler.user_controller.create_admin.assert_called_once()

    def test_handle_delete_user_by_email_success(self, mocker, capsys, caplog, mock_user_controller_class):
        '''Test method to test handle_delete_user_by_email for success'''

        user_controller = mock_user_controller_class()
        user_controller.get_all_users_by_role.return_value = self.mock_data
        self.user_handler.user_controller = user_controller
        mocker.patch('controllers.handlers.user_handler.validations.regex_validator', side_effect=[self.email])

        self.user_handler.handle_delete_user_by_email(self.role)
        captured = capsys.readouterr()

        assert LogMessage.DELETE_ENTITY, {self.role.title()} in caplog.text
        assert DisplayMessage.DELETE_USER_MSG.format(user=self.role.title()) in captured.out
        self.user_handler.user_controller.delete_user_by_email.assert_called_once()

    def test_handle_delete_user_by_email_failure(self, mocker, capsys, mock_user_controller_class):
        '''Test method to test handle_delete_user_by_email for failure'''

        user_controller = mock_user_controller_class()
        user_controller.get_all_users_by_role.return_value = self.mock_invalid_data
        self.user_handler.user_controller = user_controller
        mocker.patch('controllers.handlers.user_handler.validations.regex_validator', side_effect=[self.email])

        self.user_handler.handle_delete_user_by_email(self.role)
        captured = capsys.readouterr()

        assert DisplayMessage.DELETE_USER_FAIL_MSG.format(user=self.role.title()) in captured.out
        self.user_handler.user_controller.delete_user_by_email.assert_not_called()

    def test_handle_delete_user_by_email_no_data(self, capsys, caplog, mock_user_controller_class):
        '''Test method to test handle_delete_user_by_email'''

        user_controller = mock_user_controller_class()
        user_controller.get_all_users_by_role.return_value = None
        self.user_handler.user_controller = user_controller

        self.user_handler.handle_delete_user_by_email(self.role)
        captured = capsys.readouterr()

        assert f'No {self.role} Currently!' in caplog.text
        assert f'No {self.role} Currently!' in captured.out
        self.user_handler.user_controller.delete_user_by_email.assert_not_called()

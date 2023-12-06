'''Test file for main_menu.py'''

import pytest

from config.message_prompts import DisplayMessage, LogMessage
from menu.main_menu import MainMenu


class TestMainMenu:
    '''Test class containing test methods to test Main menu'''

    assign_menu_data = [
        ('super admin', 'super_admin_menu'),
        ('admin', 'admin_menu'),
        ('player', 'player_menu'),
        ('invalid_role', None),
    ]

    @pytest.mark.parametrize('role, expected_func_call', assign_menu_data)
    def test_assign_menu(self, mocker, role, expected_func_call, caplog, capsys):
        '''Test method to test assign_menu'''

        data = ('test_user', role, 1)
        # pylint: disable=possibly-unused-variable
        mock_super_admin_menu = mocker.patch('menu.main_menu.SuperAdminMenu.super_admin_menu')
        mock_admin_menu = mocker.patch('menu.main_menu.AdminMenu.admin_menu')
        mock_player_menu = mocker.patch('menu.main_menu.PlayerMenu.player_menu')

        MainMenu.assign_menu(data)
        captured = capsys.readouterr()

        assert LogMessage.ASSIGN_MENU in caplog.text
        if expected_func_call:
            expected_function = locals()[f'mock_{expected_func_call}']

            if expected_func_call == 'admin_menu':
                expected_function.assert_called_once_with(data[0], data[2])
            else:
                expected_function.assert_called_once_with(data[0])
        else:
            assert DisplayMessage.INVALID_ROLE_MSG in captured.out

    def test_auth_menu(self, mocker, caplog, capsys):
        '''Test method to test auth_menu'''

        data = ('test_user', 'user', 1)

        mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
        mock_assign_menu = mocker.patch.object(MainMenu, 'assign_menu')
        mock_auth_handler = mocker.patch('menu.main_menu.AuthHandler')
        mock_auth_handler().handle_login.return_value = data
        mock_auth_handler().handle_signup.return_value = data[0]
        mock_player_menu = mocker.patch('menu.main_menu.PlayerMenu.player_menu')

        MainMenu.auth_menu()
        captured = capsys.readouterr()

        assert LogMessage.RUNNING_AUTH_MENU in caplog.text
        assert DisplayMessage.APP_WELCOME_MSG in captured.out
        mock_auth_handler().handle_login.assert_called_once()
        mock_auth_handler().handle_signup.assert_called_once()
        mock_assign_menu.assert_called_once_with(data)
        mock_player_menu.assert_called_once_with(data[0])

    def test_auth_menu_invalid(self, mocker, caplog, capsys):
        '''Test method to test auth_menu with invalid login and signup'''

        mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
        mock_assign_menu = mocker.patch.object(MainMenu, 'assign_menu')
        mock_auth_handler = mocker.patch('menu.main_menu.AuthHandler')
        mock_auth_handler().handle_login.return_value = None
        mock_auth_handler().handle_signup.return_value = None
        mock_player_menu = mocker.patch('menu.main_menu.PlayerMenu.player_menu')

        MainMenu.auth_menu()
        captured = capsys.readouterr()

        assert LogMessage.RUNNING_AUTH_MENU in caplog.text
        assert DisplayMessage.APP_WELCOME_MSG in captured.out
        mock_assign_menu.assert_not_called()
        mock_player_menu.assert_not_called()

'''Test file for menu.py'''

import pytest

from src.config.message_prompts import DisplayMessage, Headers, LogMessage
from src.utils import menu

assign_menu_data = [
    ('super admin', 'super_admin_menu'),
    ('admin', 'admin_menu'),
    ('player', 'player_menu'),
    ('invalid_role', None),
]


def test_super_admin_menu(mocker, caplog, capsys):
    '''Test function to test super_admin_menu function'''

    username = 'test_super_admin'

    mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
    mock_create_admin = mocker.patch('src.utils.menu.UserHandler.handle_create_admin')
    mock_display_users = mocker.patch('src.utils.menu.UserHandler.display_users_by_role')
    mock_delete_user = mocker.patch('src.utils.menu.UserHandler.handle_delete_user_by_email')

    menu.super_admin_menu(username)
    captured = capsys.readouterr()

    assert LogMessage.RUNNING_USER_MENU, Headers.SUPER_ADMIN in caplog.text
    assert DisplayMessage.DASHBOARD_MSG.format(user=Headers.SUPER_ADMIN) in captured.out
    assert DisplayMessage.USER_WELCOME_MSG.format(user=username) in captured.out
    mock_create_admin.assert_called_once()
    mock_display_users.assert_called_once_with(role='admin')
    mock_delete_user.assert_called_once_with(role='admin')


def test_admin_menu(mocker, caplog, capsys):
    '''Test function to test admin_menu function'''

    username = 'test_admin'

    mocker.patch('builtins.input', side_effect=['1', '2', 'q'])
    mock_manage_players = mocker.patch('src.utils.menu.MenuHandler.manage_players_menu')
    mock_manage_quizzes = mocker.patch('src.utils.menu.MenuHandler.manage_quizzes_menu')
    mocker.patch('src.utils.menu.AuthHandler.handle_first_login')

    menu.admin_menu(username, 1)
    captured = capsys.readouterr()

    assert LogMessage.RUNNING_USER_MENU, Headers.ADMIN in caplog.text
    assert DisplayMessage.DASHBOARD_MSG.format(user=Headers.ADMIN) in captured.out
    assert DisplayMessage.USER_WELCOME_MSG.format(user=username) in captured.out
    mock_manage_players.assert_called_once()
    mock_manage_quizzes.assert_called_once_with(username)


def test_player_menu(mocker, caplog, capsys):
    '''Test function to test player_menu function'''

    username = 'test_player'

    mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
    mock_handle_start_quiz = mocker.patch('src.utils.menu.QuizHandler.handle_start_quiz')
    mock_display_leaderboard = mocker.patch('src.utils.menu.QuizHandler.display_leaderboard')
    mock_display_player_score = mocker.patch('src.utils.menu.UserHandler.display_player_score')

    menu.player_menu(username)
    captured = capsys.readouterr()

    assert LogMessage.RUNNING_USER_MENU, Headers.PLAYER in caplog.text
    assert DisplayMessage.DASHBOARD_MSG.format(user=Headers.PLAYER) in captured.out
    assert DisplayMessage.USER_WELCOME_MSG.format(user=username) in captured.out
    mock_handle_start_quiz.assert_called_once_with(username)
    mock_display_leaderboard.assert_called_once()
    mock_display_player_score.assert_called_once_with(username)


@pytest.mark.parametrize("role, expected_func_call", assign_menu_data)
def test_assign_menu(mocker, role, expected_func_call, caplog, capsys):
    '''Test function to test assign_menu function'''

    data = ('test_user', role, 1)

    mock_super_admin_menu = mocker.patch('src.utils.menu.super_admin_menu')
    mock_admin_menu = mocker.patch('src.utils.menu.admin_menu')
    mock_player_menu = mocker.patch('src.utils.menu.player_menu')

    menu.assign_menu(data)
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


def test_auth_menu(mocker, caplog, capsys):
    '''Test function to test start function'''

    data = ('test_user', 'user', 1)

    mocker.patch('builtins.input', side_effect=['1', '2', 'q'])
    mock_handle_login = mocker.patch('src.utils.menu.AuthHandler.handle_login', return_value=data)
    mock_handle_signup = mocker.patch('src.utils.menu.AuthHandler.handle_signup', return_value=data[0])
    mock_assign_menu = mocker.patch('src.utils.menu.assign_menu')
    mock_player_menu = mocker.patch('src.utils.menu.player_menu')

    menu.auth_menu()
    captured = capsys.readouterr()

    assert LogMessage.RUNNING_AUTH_MENU in caplog.text
    assert DisplayMessage.APP_WELCOME_MSG in captured.out
    mock_handle_login.assert_called_once()
    mock_handle_signup.assert_called_once()
    mock_assign_menu.assert_called_once_with(data)
    mock_player_menu.assert_called_once_with(data[0])

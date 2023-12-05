'''Test file for admin_menu.py'''

from config.message_prompts import DisplayMessage, Headers, LogMessage
from menu.admin_menu import AdminMenu
from utils.custom_error import DataNotFoundError


class TestAdminMenu:
    '''Test class containing test methods to test Admin menu'''

    def test_admin_menu(self, mocker, caplog, capsys):
        '''Test function to test admin_menu function'''

        username = 'test_admin'
        mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
        mock_auth_handler = mocker.patch('menu.admin_menu.AuthHandler')
        mock_manage_players = mocker.patch.object(AdminMenu, 'manage_players_menu')
        mock_manage_quizzes = mocker.patch.object(AdminMenu, 'manage_quizzes_menu')

        AdminMenu.admin_menu(username, 1)
        captured = capsys.readouterr()

        assert LogMessage.RUNNING_USER_MENU, Headers.ADMIN in caplog.text
        assert DisplayMessage.DASHBOARD_MSG.format(user=Headers.ADMIN) in captured.out
        assert DisplayMessage.USER_WELCOME_MSG.format(user=username) in captured.out
        mock_auth_handler().handle_first_login.assert_called_once_with(username, 1)
        mock_manage_players.assert_called_once()
        mock_manage_quizzes.assert_called_once_with(username)

    def test_manage_quizzes_menu(self, mocker, caplog, capsys):
        '''Test function to test manage_quizzes_menu function'''

        username = 'test_admin'
        mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
        mock_manage_players = mocker.patch.object(AdminMenu, 'manage_categories_menu')
        mock_manage_questions = mocker.patch.object(AdminMenu, 'manage_questions_menu')

        AdminMenu.manage_quizzes_menu(username)
        captured = capsys.readouterr()

        assert DisplayMessage.MANAGE_CATEGORIES_MSG in captured.out
        assert DisplayMessage.MANAGE_QUES_MSG in captured.out
        assert LogMessage.RUNNING_ADMIN_MENU, Headers.QUIZZES in caplog.text
        mock_manage_players.assert_called_once_with(username)
        mock_manage_questions.assert_called_once_with(username)

    def test_manage_players_menu(self, mocker, caplog):
        '''Test function to test manage_players_menu function'''

        role = 'player'
        mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
        mock_user_handler = mocker.patch('menu.admin_menu.UserHandler')

        AdminMenu.manage_players_menu()

        assert LogMessage.RUNNING_ADMIN_MENU, Headers.PLAYER in caplog.text
        mock_user_handler().display_users_by_role.assert_called_once_with(role=role)
        mock_user_handler().display_users_by_role.handle_delete_user_by_email(role=role)

    def test_manage_categories_menu(self, mocker, caplog, capsys):
        '''Test function to test manage_categories_menu function'''

        username = 'test_admin'
        mocker.patch('builtins.input', side_effect=['1', '2', '3', '4', '5', 'q'])
        mock_quiz_handler = mocker.patch('menu.admin_menu.QuizHandler')
        mock_quiz_handler().display_categories.side_effect = DataNotFoundError('test error')

        AdminMenu.manage_categories_menu(username)
        captured = capsys.readouterr()

        assert LogMessage.RUNNING_ADMIN_MENU, Headers.CATEGORIES in caplog.text
        assert 'test error' in caplog.text
        assert 'test error' in captured.out
        mock_quiz_handler().display_categories.assert_called_once_with(
            role='admin', header=(Headers.CATEGORY, Headers.CREATED_BY)
        )
        mock_quiz_handler().handle_create_category.assert_called_once_with(created_by=username)
        mock_quiz_handler().handle_update_category.assert_called_once()
        mock_quiz_handler().handle_delete_category.assert_called_once()

    def test_manage_questions_menu(self, mocker, caplog, capsys):
        '''Test function to test manage_questions_menu function'''

        username = 'test_admin'
        mocker.patch('builtins.input', side_effect=['1', '2', '3', '4', '5', 'q'])
        mock_quiz_handler = mocker.patch('menu.admin_menu.QuizHandler')
        mock_load_quiz_data = mocker.patch('menu.admin_menu.json_to_db_loader.load_quiz_data_from_json')

        AdminMenu.manage_questions_menu(username)
        captured = capsys.readouterr()

        assert LogMessage.RUNNING_ADMIN_MENU, Headers.QUES in caplog.text
        assert DisplayMessage.LOAD_QUES_MSG in captured.out
        mock_quiz_handler().display_all_questions.assert_called_once()
        mock_quiz_handler().display_questions_by_category.assert_called_once()
        mock_quiz_handler().handle_create_question.assert_called_once_with(created_by=username)
        mock_load_quiz_data.assert_called_once_with(created_by_admin_username=username)

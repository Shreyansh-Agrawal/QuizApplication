'''Test file for player_menu.py'''

from config.message_prompts import DisplayMessage, Headers, LogMessage
from menu.player_menu import PlayerMenu


class TestPlayerMenu:
    '''Test class containing test method to test player menu'''

    def test_player_menu(self, mocker, caplog, capsys):
        '''Test function to test player_menu function'''

        username = 'test_player'

        mocker.patch('builtins.input', side_effect=['1', '2', '3', '4', 'q'])
        mock_quiz_handler = mocker.patch('menu.player_menu.QuizHandler')
        mock_user_handler = mocker.patch('menu.player_menu.UserHandler')

        PlayerMenu.player_menu(username)
        captured = capsys.readouterr()

        assert LogMessage.RUNNING_USER_MENU, Headers.PLAYER in caplog.text
        assert DisplayMessage.DASHBOARD_MSG.format(user=Headers.PLAYER) in captured.out
        assert DisplayMessage.USER_WELCOME_MSG.format(user=username) in captured.out
        mock_quiz_handler().handle_start_quiz.assert_called_once_with(username)
        mock_quiz_handler().display_leaderboard.assert_called_once()
        mock_user_handler().display_player_score.assert_called_once_with(username)

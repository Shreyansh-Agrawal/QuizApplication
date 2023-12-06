'''Test file for quiz_handler.py'''

import pytest

from config.message_prompts import DisplayMessage, Headers, LogMessage
from controllers.handlers.quiz_handler import QuizHandler
from utils.custom_error import DataNotFoundError, DuplicateEntryError


class TestQuizHandler:
    '''Test class containing test methods for Quiz Handler class'''

    username = 'test_username'
    role = 'player'
    header = ('header', )
    mock_data = [('test_data')]
    category_name = 'test_category_name'
    error_msg = 'test error msg'
    quiz_handler = QuizHandler()

    @pytest.fixture(autouse=True)
    def mock_pretty_print(self, mocker):
        '''Test fixture to mock pretty print'''

        return mocker.patch('controllers.handlers.quiz_handler.pretty_print')

    @pytest.fixture
    def mock_quiz_controller_class(self, mocker):
        '''Test fixture to mock QuizController class'''

        return mocker.patch('controllers.handlers.quiz_handler.QuizController')

    @pytest.fixture
    def mock_create_quiz_helper_class(self, mocker):
        '''Test fixture to mock CreateQuizHelper class'''

        return mocker.patch('controllers.handlers.quiz_handler.CreateQuizHelper')

    @pytest.fixture
    def mock_start_quiz_helper_class(self, mocker):
        '''Test fixture to mock StartQuizHelper class'''

        return mocker.patch('controllers.handlers.quiz_handler.StartQuizHelper')

    def test_display_categories(self, mocker, caplog, capsys, mock_create_quiz_helper_class):
        '''Test method to test display_categories'''

        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_categories(self.role, self.header)
        captured = capsys.readouterr()

        assert LogMessage.DISPLAY_ALL_ENTITY, Headers.CATEGORY in caplog.text
        assert DisplayMessage.CATEGORIES_MSG in captured.out
        mock_pretty_print.assert_called_once()

    def test_display_categories_error(self, mocker, mock_create_quiz_helper_class):
        '''Test method to test display_categories error'''

        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = None
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        with pytest.raises(DataNotFoundError):
            self.quiz_handler.display_categories(self.role, self.header)

        mock_pretty_print.assert_not_called()

    def test_display_all_questions(self, mocker, caplog, capsys, mock_quiz_controller_class):
        '''Test method to test display_all_questions'''

        quiz_controller = mock_quiz_controller_class()
        quiz_controller.get_all_questions.return_value = self.mock_data
        self.quiz_handler.quiz_controller = quiz_controller
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_all_questions()
        captured = capsys.readouterr()

        assert LogMessage.DISPLAY_ALL_ENTITY, Headers.QUES in caplog.text
        assert DisplayMessage.QUES_MSG in captured.out
        mock_pretty_print.assert_called_once()

    def test_display_all_questions_no_data(self, mocker, mock_quiz_controller_class):
        '''Test method to test display_all_questions when no data'''

        quiz_controller = mock_quiz_controller_class
        quiz_controller.get_all_questions.return_value = None
        self.quiz_handler.quiz_controller = quiz_controller
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_all_questions()
        mock_pretty_print.assert_not_called()

    def test_display_questions_by_category(self, mocker, caplog, capsys, mock_create_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test display_questions_by_category'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper

        quiz_controller = mock_quiz_controller_class()
        quiz_controller.get_questions_by_category.return_value = self.mock_data
        self.quiz_handler.quiz_controller = quiz_controller

        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', return_value = '1')
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_questions_by_category()
        captured = capsys.readouterr()

        assert DisplayMessage.DISPLAY_QUES_IN_A_CATEGORY_MSG.format(name=self.mock_data[0][0]) in captured.out
        assert LogMessage.DISPLAY_QUES_BY_CATEGORY in caplog.text
        mock_pretty_print.assert_called_once()

    def test_display_questions_by_category_invalid_category(self, mocker, caplog, capsys, mock_create_quiz_helper_class):
        '''Test method to test display_questions_by_category when invalid category selected'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper

        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', return_value = '0')
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_questions_by_category()
        captured = capsys.readouterr()

        assert LogMessage.DISPLAY_QUES_BY_CATEGORY in caplog.text
        assert 'No such Category! Please choose from above!!' in caplog.text
        assert 'No such Category! Please choose from above!!' in captured.out
        mock_pretty_print.assert_not_called()

    def test_display_questions_by_category_no_question(self, mocker, caplog, capsys, mock_create_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test display_questions_by_category when no question present in that category'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        quiz_controller = mock_quiz_controller_class()
        quiz_controller.get_questions_by_category.return_value = None
        self.quiz_handler.quiz_controller = quiz_controller
        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', return_value = '1')
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_questions_by_category()
        captured = capsys.readouterr()

        assert DisplayMessage.QUES_NOT_FOUND_MSG in captured.out
        assert LogMessage.DISPLAY_QUES_BY_CATEGORY in caplog.text
        mock_pretty_print.assert_not_called()

    def test_display_leaderboard(self, mocker, capsys, mock_quiz_controller_class):
        '''Test method to test display_leaderboard'''

        quiz_controller = mock_quiz_controller_class()
        quiz_controller.get_leaderboard.return_value = self.mock_data
        self.quiz_handler.quiz_controller = quiz_controller
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_leaderboard()
        captured = capsys.readouterr()

        assert DisplayMessage.LEADERBOARD_MSG in captured.out
        mock_pretty_print.assert_called_once()

    def test_display_leaderboard_no_data(self, mocker, capsys, caplog, mock_quiz_controller_class):
        '''Test method to test display_leaderboard when no data present'''

        quiz_controller = mock_quiz_controller_class()
        quiz_controller.get_leaderboard.return_value = None
        self.quiz_handler.quiz_controller = quiz_controller
        mock_pretty_print = mocker.patch('controllers.handlers.quiz_handler.pretty_print')

        self.quiz_handler.display_leaderboard()
        captured = capsys.readouterr()

        assert LogMessage.LEADERBOARD_DATA_NOT_FOUND in caplog.text
        assert DisplayMessage.QUIZ_DATA_NOT_FOUND_MSG in captured.out
        mock_pretty_print.assert_not_called()

    def test_handle_start_quiz(self, mocker, caplog, capsys, mock_start_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test handle_start_quiz'''

        mocker.patch('builtins.input', side_effect=['1', '2', '3', 'q'])
        start_quiz_helper = mock_start_quiz_helper_class()
        start_quiz_helper.select_category.return_value = self.mock_data
        self.quiz_handler.start_quiz_helper = start_quiz_helper
        quiz_controller = mock_quiz_controller_class()
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_start_quiz(self.username)
        captured = capsys.readouterr()

        assert LogMessage.START_QUIZ, self.username in caplog.text
        assert DisplayMessage.WRONG_INPUT_MSG in captured.out

    def test_handle_start_quiz_invalid_category(self, mocker, caplog, capsys, mock_start_quiz_helper_class):
        '''Test method to test handle_start_quiz with invalid category'''

        mocker.patch('builtins.input', side_effect=['1'])
        start_quiz_helper = mock_start_quiz_helper_class()
        start_quiz_helper.select_category.side_effect = DataNotFoundError(self.error_msg)
        self.quiz_handler.start_quiz_helper = start_quiz_helper

        self.quiz_handler.handle_start_quiz(self.username)
        captured = capsys.readouterr()

        assert self.error_msg in caplog.text
        assert self.error_msg in captured.out

    def test_handle_start_quiz_no_data(self, mocker, caplog, capsys, mock_quiz_controller_class):
        '''Test method to test handle_start_quiz with no quiz data'''

        mocker.patch('builtins.input', side_effect=['2'])
        quiz_controller = mock_quiz_controller_class()
        quiz_controller.start_quiz.side_effect = DataNotFoundError(self.error_msg)
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_start_quiz(self.username)
        captured = capsys.readouterr()

        assert self.error_msg in caplog.text
        assert self.error_msg in captured.out

    def test_handle_create_category(self, mocker, caplog, capsys, mock_quiz_controller_class):
        '''Test method to test handle_create_category'''

        mocker.patch.object(QuizHandler, 'display_categories', side_effect=DataNotFoundError(self.error_msg))
        mocker.patch('controllers.handlers.quiz_handler.DAO.read_from_database', return_value=self.mock_data)
        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', return_value=self.category_name)
        quiz_controller = mock_quiz_controller_class()
        self.quiz_handler.quiz_controller = quiz_controller
        self.quiz_handler.quiz_controller.create_category.side_effect = DuplicateEntryError(self.error_msg)

        self.quiz_handler.handle_create_category(self.username)
        captured = capsys.readouterr()

        assert self.error_msg in caplog.text
        assert self.error_msg in captured.out
        assert DisplayMessage.CREATE_CATEGORY_MSG in captured.out

    def test_handle_create_question(self, mocker, capsys, caplog, mock_quiz_controller_class):
        '''Test method to test handle_create_question with no categories to display'''

        mocker.patch.object(QuizHandler, 'display_categories', side_effect=DataNotFoundError(self.error_msg))
        quiz_controller = mock_quiz_controller_class()
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_create_question(self.username)
        captured = capsys.readouterr()

        assert self.error_msg in caplog.text
        assert self.error_msg in captured.out

    def test_handle_create_question_duplicate_ques(self, mocker, capsys, caplog, mock_quiz_controller_class):
        '''Test method to test handle_create_question when duplicate question is created'''

        mocker.patch.object(QuizHandler, 'display_categories')
        quiz_controller = mock_quiz_controller_class()
        quiz_controller.create_question.side_effect = DuplicateEntryError(self.error_msg)
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_create_question(self.username)
        captured = capsys.readouterr()

        assert self.error_msg in caplog.text
        assert self.error_msg in captured.out

    def test_handle_update_category(self, mocker, capsys, caplog, mock_create_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test handle_update_category with duplicate category'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', side_effect=['1', self.category_name])
        quiz_controller = mock_quiz_controller_class()
        quiz_controller.update_category_by_name.side_effect = DuplicateEntryError(self.error_msg)
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_update_category()
        captuted = capsys.readouterr()

        assert DisplayMessage.UPDATE_CATEGORY_MSG in captuted.out
        assert self.error_msg in caplog.text
        assert self.error_msg in captuted.out
        self.quiz_handler.quiz_controller.update_category_by_name.assert_called_once()

    def test_handle_update_category_invalid_category(self, mocker, capsys, caplog, mock_create_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test handle_update_category with invalid category'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', side_effect=['-1', self.category_name])
        quiz_controller = mock_quiz_controller_class()
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_update_category()
        captured = capsys.readouterr()

        assert 'No such Category! Please choose from above!!' in caplog.text
        assert 'No such Category! Please choose from above!!' in captured.out
        self.quiz_handler.quiz_controller.update_category_by_name.assert_not_called()

    def test_handle_delete_category(self, mocker, capsys, caplog, mock_create_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test_handle_delete_category'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', return_value = '1')
        mocker.patch('builtins.input', return_value = 'yes')
        quiz_controller = mock_quiz_controller_class()
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_delete_category()
        captured = capsys.readouterr()

        assert LogMessage.DELETE_ENTITY, Headers.CATEGORY in caplog.text
        assert DisplayMessage.DELETE_CATEGORY_MSG in captured.out
        self.quiz_handler.quiz_controller.delete_category_by_name.assert_called_once()

    def test_handle_delete_category_invalid_category(self, mocker, capsys, caplog, mock_create_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test_handle_delete_category with invalid category'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', return_value = '-1')
        mocker.patch('builtins.input', return_value = 'yes')
        quiz_controller = mock_quiz_controller_class()
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_delete_category()
        captured = capsys.readouterr()

        assert 'No such Category! Please choose from above!!' in caplog.text
        assert 'No such Category! Please choose from above!!' in captured.out
        self.quiz_handler.quiz_controller.delete_category_by_name.assert_not_called()

    def test_handle_delete_category_cancelled(self, mocker, mock_create_quiz_helper_class, mock_quiz_controller_class):
        '''Test method to test_handle_delete_category when deletion is cancelled'''

        mocker.patch.object(QuizHandler, 'display_categories')
        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        self.quiz_handler.create_quiz_helper = create_quiz_helper
        mocker.patch('controllers.handlers.quiz_handler.validations.regex_validator', return_value = '1')
        mocker.patch('builtins.input', return_value = 'no')
        quiz_controller = mock_quiz_controller_class()
        self.quiz_handler.quiz_controller = quiz_controller

        self.quiz_handler.handle_delete_category()

        self.quiz_handler.quiz_controller.delete_category_by_name.assert_not_called()

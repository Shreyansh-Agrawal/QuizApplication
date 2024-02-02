'''Test file for quiz_controller.py'''

import pymysql

import pytest

from config.string_constants import DisplayMessage, Headers, LogMessage
from controllers.quiz_controller import QuizController
from utils.custom_error import DataNotFoundError, DuplicateEntryError


class TestQuizController:
    '''Test class containing test methods to test Quiz Controller methods'''

    data = [('test data')]
    category_name = 'test_category'
    old_category_name = 'test_old_category'
    username = 'test_username'
    question_data = [
        ('Q030', 'What is the result of 6 squared?', 'ONE WORD', '36'),
        ('Q108', 'Which strait separates Europe from Asia?', 'MCQ', 'Bosporus Strait'),
        ('Q110', 'Which river is often called the "Cradle of Civilization"?', 'MCQ', 'Tigris and Euphrates'),
        ('Q043', 'What is the value of the mathematical constant "π" (pi) to two decimal places?', 'ONE WORD', '3.14'),
        ('Q029', 'What is the next prime number after 7?', 'ONE WORD', '11'),
        ('Q104', 'Which mountain range is considered the "Roof of the World"?', 'MCQ', 'Himalayas'),
        ('Q115', 'Which African country is located at the southernmost tip of the continent?', 'MCQ', 'South Africa'),
        ('Q011', 'The process of converting sugar into alcohol is known as what?', 'ONE WORD', 'Fermentation'),
        ('Q009', 'How many bones are there in the adult human body?', 'ONE WORD', '206'),
        ('Q015', 'Is water a conductor of electricity? (True/False)', 'T/F', 'True')
    ]
    option_data = [
        [('36',)],
        [('Bosporus Strait',), ('Strait of Gibraltar',), ('Malacca Strait',), ('Hormuz Strait',)],
        [('Nile',), ('Amazon',), ('Tigris and Euphrates',), ('Yangtze',)],
        [('3.14',)],
        [('11',)],
        [('Rocky Mountains',), ('Andes',), ('Alps',), ('Himalayas',)],
        [('Egypt',), ('South Africa',), ('Nigeria',), ('Morocco',)],
        [('Fermentation',)],
        [('206',)],
        [('True',)]
    ]
    player_response_data = ['35', 4, 1, '3.14', '11', 4, 2, 'fermentation', '206', 'true']
    score = 70
    quiz_controller = QuizController()

    @pytest.fixture
    def mock_read(self, mocker):
        '''Test fixture to mock read method'''

        return mocker.patch('controllers.quiz_controller.db.read', return_value=self.data)

    @pytest.fixture
    def mock_write(self, mocker):
        '''Test fixture to mock write method'''

        return mocker.patch('controllers.quiz_controller.db.write')

    @pytest.fixture
    def mock_category_class(self, mocker):
        '''Test fixture to mock Category class'''

        return mocker.patch('controllers.quiz_controller.Category')

    @pytest.fixture
    def mock_create_quiz_helper_class(self, mocker):
        '''Test fixture to mock CreateQuizHelper class'''

        return mocker.patch('controllers.quiz_controller.CreateQuizHelper')

    @pytest.fixture
    def mock_start_quiz_helper_class(self, mocker):
        '''Test fixture to mock StartQuizHelper class'''

        return mocker.patch('controllers.quiz_controller.StartQuizHelper')

    def test_get_all_questions(self, mock_read):
        '''Test method to test get_all_questions'''

        expected = mock_read()
        result = self.quiz_controller.get_all_questions()
        assert result == expected

    def test_get_questions_by_category(self, mock_read, caplog):
        '''Test method to test get_questions_by_category'''

        expected = mock_read()
        result = self.quiz_controller.get_questions_by_category(self.category_name)

        assert LogMessage.GET_QUES_BY_CATEGORY in caplog.text
        assert result == expected

    def test_get_leaderboard(self, mock_read):
        '''Test method to test get_leaderboard'''

        expected = mock_read()
        result = self.quiz_controller.get_leaderboard()
        assert result == expected

    def test_create_category_success(self, mock_category_class, capsys, caplog):
        '''Test method to test create_category success'''

        mock_category = mock_category_class()
        self.quiz_controller.create_category(self.data)
        captured = capsys.readouterr()

        assert LogMessage.CREATE_ENTITY, Headers.CATEGORY in caplog.text
        assert LogMessage.CREATE_SUCCESS, Headers.CATEGORY in caplog.text
        assert DisplayMessage.CREATE_CATEGORY_SUCCESS_MSG in captured.out
        mock_category.save_to_database.assert_called_once()

    def test_create_category_error(self, mock_category_class):
        '''Test method to test create_category error'''

        mock_category = mock_category_class()
        mock_category.save_to_database.side_effect = pymysql.err.IntegrityError

        with pytest.raises(DuplicateEntryError):
            self.quiz_controller.create_category(self.data)

    def test_create_question_success(self, mock_create_quiz_helper_class, mocker, capsys, caplog):
        '''Test method to test create_question success'''

        mock_create_quiz_helper = mock_create_quiz_helper_class()
        mock_question = mocker.Mock()
        mock_create_quiz_helper.create_option.return_value = mock_question
        self.quiz_controller.create_question(self.username)
        captured = capsys.readouterr()

        assert LogMessage.CREATE_SUCCESS, Headers.QUES in caplog.text
        assert DisplayMessage.CREATE_QUES_SUCCESS_MSG in captured.out
        mock_question.save_to_database.assert_called_once()

    def test_create_question_error(self, mock_create_quiz_helper_class, mocker):
        '''Test method to test create_question error'''

        mock_create_quiz_helper = mock_create_quiz_helper_class()
        mock_question = mocker.Mock()
        mock_create_quiz_helper.create_option.return_value = mock_question
        mock_question.save_to_database.side_effect = pymysql.err.IntegrityError

        with pytest.raises(DuplicateEntryError):
            self.quiz_controller.create_question(self.username)

    @pytest.mark.usefixtures('mock_write')
    def test_update_category_by_name_success(self, caplog, capsys):
        '''Test method to test update_category_by_name success'''

        self.quiz_controller.update_category_by_name(self.old_category_name, self.category_name)
        captured = capsys.readouterr()

        assert LogMessage.UPDATE_ENTITY, Headers.CATEGORY in caplog.text
        assert f'Category {self.old_category_name} updated to {self.category_name}' in caplog.text
        assert DisplayMessage.UPDATE_CATEGORY_SUCCESS_MSG.format(
            name=self.old_category_name, new_name=self.category_name
        ) in captured.out


    def test_update_category_by_name_error(self, caplog, mock_write):
        '''Test method to test update_category_by_name error'''

        mock_write.side_effect = pymysql.err.IntegrityError
        with pytest.raises(DuplicateEntryError):
            self.quiz_controller.update_category_by_name(self.old_category_name, self.category_name)
        assert LogMessage.UPDATE_ENTITY, Headers.CATEGORY in caplog.text

    @pytest.mark.usefixtures('mock_write')
    def test_delete_category_by_name_success(self, capsys, caplog):
        '''Test method to test delete_category_by_name success'''

        self.quiz_controller.delete_category_by_name(self.category_name)
        captured = capsys.readouterr()

        assert LogMessage.DELETE_CATEGORY, self.category_name in caplog.text
        assert LogMessage.DELETE_CATEGORY_SUCCESS, self.category_name in caplog.text
        assert DisplayMessage.DELETE_CATEGORY_SUCCESS_MSG.format(name=self.category_name) in captured.out

    def test_start_quiz_with_category(self, mocker, mock_start_quiz_helper_class, caplog, capsys):
        '''Test method to test start quiz method in simple mode'''

        mock_start_quiz_helper = mock_start_quiz_helper_class()
        mock_start_quiz_helper.get_random_questions_by_category.return_value = self.question_data
        mock_read = mocker.patch('controllers.quiz_controller.db.read')
        mock_read.side_effect = self.option_data
        mock_start_quiz_helper.get_player_response.side_effect = self.player_response_data

        self.quiz_controller.start_quiz(self.username, self.category_name)
        captured = capsys.readouterr()

        assert LogMessage.COMPLETE_QUIZ, self.username in caplog.text
        assert LogMessage.START_QUIZ, self.username in caplog.text
        assert DisplayMessage.QUIZ_START_MSG in captured.out
        assert DisplayMessage.DISPLAY_SCORE_MSG.format(score=self.score) in captured.out
        assert DisplayMessage.REVIEW_RESPONSES_MSG in captured.out
        mock_start_quiz_helper.save_quiz_score.assert_called_once_with(self.username, self.score)

    def test_start_quiz_without_category_error(self, mock_start_quiz_helper_class):
        '''Test method to test start quiz method in random mode with error'''

        mock_start_quiz_helper = mock_start_quiz_helper_class()
        mock_start_quiz_helper.get_random_questions.return_value = self.data

        with pytest.raises(DataNotFoundError):
            self.quiz_controller.start_quiz(self.username)

        mock_start_quiz_helper.save_quiz_score.assert_not_called()

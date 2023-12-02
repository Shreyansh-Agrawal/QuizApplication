'''Test file for start_quiz_helper.py'''

from datetime import datetime, timezone

import pytest

from src.config.message_prompts import LogMessage
from src.controllers.helpers.start_quiz_helper import StartQuizHelper
from utils.custom_error import DataNotFoundError


class TestStartQuizHelper:
    '''Test class containing test methods to test StartQuizHelper methods'''

    username = 'test_username'
    role = 'player'
    score = 70
    header = ('header', )
    mock_data = [('test_data', ), ('other_data', )]
    category_name = 'test_category_name'
    ques_type_data = [
        ('1', {'question_type': 'MCQ'}),
        ('2', {'question_type': 'T/F'}),
        ('3', {'question_type': 'ONE WORD'})
    ]
    create_option_data = [
        ('MCQ', ['Answer', 'Option 1', 'Option 2', 'Option 3'], 4),
        ('T/F', ['Answer'], 1),
        ('ONE WORD', ['Answer'], 1),
        ('Invalid', [], 0)
    ]
    display_ques_data = [
        (
            1,
            'What is the capital of France?',
            'MCQ',
            [('Paris',), ('Rome',), ('Berlin',), ('Madrid',)],
            '\n1) What is the capital of France?\n    1. Paris\n    2. Rome\n    3. Berlin\n    4. Madrid\n'
        ),
        (
            1,
            'Is the earth flat?',
            'T/F',
            [('True',), ('False',)],
            '\n\n1) Is the earth flat?\n   1. True\n   2. False\n'
        )
    ]
    player_response_data = [
            ('MCQ', ['5', '3'], 3),  # Out of range option, then correct option
            ('T/F', ['3', '2'], 'false'),  # Out of range option, then false option
            ('T/F', ['3', '1'], 'true'),  # Out of range option, then true option
            ('ONE WORD', ['Text'], 'Text'),  # Text input for one-word answer
    ]
    start_quiz_helper = StartQuizHelper()

    @pytest.fixture(autouse=True)
    def mock_pretty_print(self, mocker):
        '''Test fixture to mock pretty print'''

        return mocker.patch('src.controllers.helpers.start_quiz_helper.pretty_print')

    @pytest.fixture(autouse=True)
    def mock_read_from_database(self, mocker):
        '''Test fixture to mock read_from_database method'''

        mocker.patch('src.controllers.helpers.start_quiz_helper.DAO.read_from_database', return_value=self.mock_data)

    @pytest.fixture(autouse=True)
    def mock_write_to_database(self, mocker):
        '''Test fixture to mock write_to_database method'''

        mocker.patch('src.controllers.helpers.start_quiz_helper.DAO.write_to_database')

    @pytest.fixture
    def mock_create_quiz_helper_class(self, mocker):
        '''Test fixture to mock CreateQuizHelper class'''

        return mocker.patch('src.controllers.helpers.start_quiz_helper.CreateQuizHelper')

    def test_get_random_questions(self):
        '''Test method to test get_random_questions'''

        result = self.start_quiz_helper.get_random_questions()
        assert result == self.mock_data

    def test_get_random_questions_by_category(self):
        '''Test method to test get_random_questions_by_category'''

        result = self.start_quiz_helper.get_random_questions_by_category(self.category_name)
        assert result == self.mock_data

    def test_select_category(self, mocker, mock_create_quiz_helper_class):
        '''Test method to test select_category'''

        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        mocker.patch('src.controllers.helpers.start_quiz_helper.validations.regex_validator', return_value = '1')

        result = self.start_quiz_helper.select_category()

        assert result == self.mock_data[0][0]

    def test_select_category_no_data(self, mock_create_quiz_helper_class):
        '''Test method to test select_category when no data is present'''

        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = None

        with pytest.raises(DataNotFoundError):
            self.start_quiz_helper.select_category()

    def test_select_category_invalid_category(self, mocker, mock_create_quiz_helper_class):
        '''Test method to test select_category when invalid category is selected'''

        create_quiz_helper = mock_create_quiz_helper_class()
        create_quiz_helper.get_all_categories.return_value = self.mock_data
        mocker.patch('src.controllers.helpers.start_quiz_helper.validations.regex_validator', return_value = '-1')

        with pytest.raises(DataNotFoundError):
            self.start_quiz_helper.select_category()

    @pytest.mark.parametrize('question_no, question, question_type, options_data, expected_output', display_ques_data)
    def test_display_question(self, capsys, question_no, question, question_type, options_data, expected_output):
        '''Test method to test display_question'''

        self.start_quiz_helper.display_question(question_no, question, question_type, options_data)
        captured = capsys.readouterr()
        assert captured.out in expected_output

    @pytest.mark.parametrize('question_type, user_input, expected_output', player_response_data)
    def test_get_player_response(self, mocker, question_type, user_input, expected_output):
        '''Test method to test get_player_response'''

        mocker.patch('src.controllers.helpers.start_quiz_helper.validations.regex_validator', side_effect = user_input)
        result = self.start_quiz_helper.get_player_response(question_type)
        assert result == expected_output

    def test_save_quiz_score(self, mocker, caplog):
        '''Test method to test save_quiz_score'''

        mocker.patch('src.controllers.helpers.start_quiz_helper.validations.validate_id')
        mock_datetime = mocker.patch('src.controllers.helpers.start_quiz_helper.datetime')
        mock_time = datetime(2023, 12, 1, 10, 30, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_time

        self.start_quiz_helper.save_quiz_score(self.username, self.score)
        assert LogMessage.SAVE_QUIZ_SCORE, self.username in caplog.text
        assert LogMessage.SAVE_QUIZ_SCORE_SUCCESS, self.username in caplog.text

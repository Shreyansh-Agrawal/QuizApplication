'''Test file for quiz.py'''

import pytest

from src.models.quiz import Category, Option, Question, QuizEntity
from utils.custom_error import DataNotFoundError


class TestQuizEntity:
    '''Test class containing tests for QuizEntity class'''

    def test_quiz_entity_instance_creation(self):
        '''Test method to test QuizEntity class instance creation'''

        text = 'Test Question'
        quiz_entity = 'question'

        quiz_entity_obj = QuizEntity(text, quiz_entity)

        assert quiz_entity_obj.text == text
        assert quiz_entity_obj.entity_id is not None


class TestCategory:
    '''Test class containing tests for Category class'''

    def test_category_instance_creation(self, category_data):
        '''Test method to test Category class instance creation'''

        category = Category(category_data)

        assert category.text == category_data['category_name']
        assert category.entity_id is not None
        assert category.admin_id == category_data['admin_id']
        assert category.admin_username == category_data['admin_username']

    def test_category_save_to_database(self, category_data, mocker):
        '''Test method to test Category class save_to_database method'''

        mock_write_to_database = mocker.patch('src.models.quiz.DAO.write_to_database')
        category = Category(category_data)
        category.save_to_database()

        mock_write_to_database.assert_called_once()


class TestOption:
    '''Test class containing tests for Option class'''

    def test_option_instance_creation(self, option_data):
        '''Test method to test Option class instance creation'''

        option = Option(option_data)

        assert option.text == option_data['option_text']
        assert option.entity_id is not None
        assert option.question_id == option_data['question_id']
        assert option.is_correct == option_data['is_correct']

    def test_option_save_to_database(self, option_data, mocker):
        '''Test method to test Option class save_to_database method'''

        mock_write_to_database = mocker.patch('src.models.quiz.DAO.write_to_database')
        option = Option(option_data)
        option.save_to_database()

        mock_write_to_database.assert_called_once()


class TestQuestion:
    '''Test class containing tests for Question class'''

    def test_question_instance_creation(self, question_data):
        '''Test method to test Question class instance creation'''

        question = Question(question_data)

        assert question.text == question_data['question_text']
        assert question.entity_id is not None
        assert question.category_id == question_data['category_id']
        assert question.admin_id == question_data['admin_id']
        assert question.admin_username == question_data['admin_username']
        assert question.question_type == question_data['question_type']
        assert not question.options

    def test_add_option(self, question_data, mocker):
        '''Test method to test Question class add_option method'''

        question = Question(question_data)
        option = mocker.Mock()
        question.add_option(option)

        assert len(question.options) == 1
        assert question.options[0] == option

    def test_question_save_to_database_with_options(self, question_data, mocker):
        '''Test method to test Question class save_to_database method'''

        mock_write_to_database = mocker.patch('src.models.quiz.DAO.write_to_database')
        mock_option = mocker.Mock()
        question = Question(question_data)
        question.add_option(mock_option)
        question.save_to_database()

        mock_write_to_database.assert_called_once()
        mock_option.save_to_database.assert_called_once()

    def test_question_save_to_database_without_option(self, question_data, mocker):
        '''Test method to test Question class save_to_database method without adding option'''

        mock_write_to_database = mocker.patch('src.models.quiz.DAO.write_to_database')
        mock_option = mocker.Mock()
        question = Question(question_data)

        with pytest.raises(DataNotFoundError):
            question.save_to_database()

        mock_write_to_database.assert_not_called()
        mock_option.save_to_database.assert_not_called()

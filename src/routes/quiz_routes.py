'Routes for the Quiz related functionalities'

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint

from config.message_prompts import Roles
from controllers.quiz_controller import QuizController
from database.database_access import DatabaseAccess
from schemas.quiz import AnswerSchema
from utils.rbac import access_level

blp = Blueprint('Quiz', __name__, description='Routes for the Quiz related functionalities')
db = DatabaseAccess()
quiz_controller = QuizController(db)


@blp.route('/leaderboard')
class Leaderboard(MethodView):
    '''
    Routes to:
        Get leaderboard details
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    def get(self):
        'Get leaderboard details'
        return quiz_controller.get_leaderboard()


@blp.route('/scores/me')
class Score(MethodView):
    '''
    Routes to:
        Get player's past scores
    '''

    @access_level(roles=[Roles.PLAYER])
    def get(self):
        'Get past scores of a player'
        player_id = get_jwt_identity()
        return quiz_controller.get_player_scores(player_id)


@blp.route('/quiz')
class Quiz(MethodView):
    '''
    Routes to:
        Get random questions for quiz
    '''

    @access_level(roles=[Roles.PLAYER])
    def get(self):
        '''
        Get random questions for quiz
        Query Parameters: category_id
        '''
        category_id = request.args.get('category_id')
        return quiz_controller.get_random_questions(category_id)


@blp.route('/quiz/answers')
class QuizAnswer(MethodView):
    '''
    Routes to:
        Post player responses to the questions
    '''

    @access_level(roles=[Roles.PLAYER])
    @blp.arguments(AnswerSchema(many=True))
    def post(self, player_answers):
        'Post player responses to the questions'
        player_id = get_jwt_identity()
        return quiz_controller.evaluate_player_answers(player_id, player_answers)
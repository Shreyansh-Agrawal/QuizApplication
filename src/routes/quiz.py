'Routes for the Quiz related functionalities'

from flask.views import MethodView
from flask_smorest import Blueprint

from config.message_prompts import Roles
from utils.rbac import access_level

blp = Blueprint('Quiz', __name__)


@blp.route('/leaderboard')
class Leaderboard(MethodView):
    '''
    Routes to:
        Get leaderboard details
    '''

    @access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
    def get(self):
        'Get leaderboard details'


@blp.route('/scores/<string:player_id>')
class ScoreByPlayerId(MethodView):
    '''
    Routes to:
        Get player's past scores
    '''

    @access_level(roles=[Roles.PLAYER])
    def get(self, player_id):
        'Get past scores of a player'


@blp.route('/quizzes')
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


@blp.route('/quizzes/answers')
class QuizAnswer(MethodView):
    '''
    Routes to:
        Post player responses to the questions
    '''

    @access_level(roles=[Roles.PLAYER])
    def post(self):
        'Post player responses to the questions'

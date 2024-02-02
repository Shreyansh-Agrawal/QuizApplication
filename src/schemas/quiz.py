'Schema for Quiz data'

from marshmallow import fields, validate
from config.string_constants import QUESTION_TYPES

from config.regex_patterns import RegexPattern
from schemas.config_schema import CustomSchema, ResponseSchema


class AnswerSchema(CustomSchema):
    'Schema for player answers'

    question_id = fields.Str(required=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    user_answer = fields.Str(required=True, validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))


class QuizParamsSchema(CustomSchema):
    'Schema for query parameters while fetching questions for quiz'

    category_id = fields.Str(required=False, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    question_type = fields.Str(required=False, validate=validate.OneOf(QUESTION_TYPES))
    limit = fields.Int(required=False, validate=validate.Range(min=1))


class LeaderboardDataSchema(CustomSchema):
    'Schema for leaderboard data'

    player_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    username = fields.Str(required=True, validate=validate.Regexp(RegexPattern.USERNAME_PATTERN))
    score = fields.Int(dump_only=True, validate=validate.Range(min=0, max=100))
    timestamp = fields.Str(dump_only=True)


class LeaderboardResponseSchema(ResponseSchema):
    'Schema for leaderboard response'

    data = fields.Nested(LeaderboardDataSchema, many=True)


class ScoreDataSchema(CustomSchema):
    'Schema for score data'

    score_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    score = fields.Int(dump_only=True, validate=validate.Range(min=0, max=100))
    timestamp = fields.Str(dump_only=True)


class ScoreResponseSchema(ResponseSchema):
    'Schema for score response'

    data = fields.Nested(ScoreDataSchema, many=True)


class QuizQuestionDataSchema(CustomSchema):
    'Schema for quiz questions data'

    question_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    question_text = fields.Str(required=True, validate=validate.Regexp(RegexPattern.QUES_TEXT_PATTERN))
    question_type = fields.Str(required=True, validate=validate.OneOf(QUESTION_TYPES))
    options = fields.List(fields.Str(validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN)))


class QuizQuestionResponseSchema(ResponseSchema):
    'Schema for quiz questions response'

    data = fields.Nested(QuizQuestionDataSchema, many=True)


class ResponseDataSchema(CustomSchema):
    'Schema for user responses to quiz'

    question_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    question_text = fields.Str(required=True, validate=validate.Regexp(RegexPattern.QUES_TEXT_PATTERN))
    user_answer = fields.Str(validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))
    correct_answer = fields.Str(validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))
    is_correct = fields.Bool()


class QuizAnswerDataSchema(CustomSchema):
    'Schema for quiz answers data'

    score = fields.Int(dump_only=True, validate=validate.Range(min=0, max=100))
    responses = fields.Nested(ResponseDataSchema, many=True)


class QuizAnswerResponseSchema(ResponseSchema):
    'Schema for quiz answers response'

    data = fields.Nested(QuizAnswerDataSchema)

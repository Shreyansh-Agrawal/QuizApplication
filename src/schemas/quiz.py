'Schema for Quiz data'

from marshmallow import fields, validate
from config.message_prompts import QUESTION_TYPES

from config.regex_patterns import RegexPattern
from schemas.config_schema import CustomSchema


class AnswerSchema(CustomSchema):
    'Schema for player answers'

    question_id = fields.Str(required=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    user_answer = fields.Str(required=True, validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))


class QuizParamsSchema(CustomSchema):
    'Schema for query parameters while fetching questions for quiz'
    
    category_id = fields.Str(required=False, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    question_type = fields.Str(required=False, validate=validate.OneOf(QUESTION_TYPES))
    limit = fields.Int(required=False, validate=validate.Range(min=1))

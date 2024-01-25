'Schema for Quiz data'

from marshmallow import fields, validate

from config.regex_patterns import RegexPattern
from schemas.config_schema import CustomSchema


class AnswerSchema(CustomSchema):
    'Schema for player answers'

    question_id = fields.Str(required=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    user_answer = fields.Str(required=True, validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))

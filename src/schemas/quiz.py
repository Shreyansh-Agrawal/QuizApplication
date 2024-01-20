'Schema for Quiz data'

from marshmallow import Schema, fields, validate

from config.regex_patterns import RegexPattern


class AnswerSchema(Schema):
    'Schema for player answers'

    question_id = fields.Str(required=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    user_answer = fields.Str(required=True, validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))

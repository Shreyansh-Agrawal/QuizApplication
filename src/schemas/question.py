'Schema for Question data'

from marshmallow import fields, validate

from config.regex_patterns import RegexPattern
from config.string_constants import QUESTION_TYPES
from schemas.config_schema import CustomSchema, ResponseSchema


class QuestionSchema(CustomSchema):
    'Schema for Question data'

    category_name = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    question_text = fields.Str(required=True, validate=validate.Regexp(RegexPattern.QUES_TEXT_PATTERN))
    question_type = fields.Str(required=True, validate=validate.OneOf(QUESTION_TYPES))
    answer = fields.Str(required=True, validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))
    other_options = fields.List(fields.Str(validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN)))


class QuestionOptionsSchema(CustomSchema):
    'Schema for Options data'

    answer = fields.Str(required=True, validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))
    other_options = fields.List(fields.Str(validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN)), missing=[])


class QuizQuestionSchema(CustomSchema):
    'Schema for Quiz Question data'

    question_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    question_text = fields.Str(required=True, validate=validate.Regexp(RegexPattern.QUES_TEXT_PATTERN))
    question_type = fields.Str(required=True, validate=validate.OneOf(QUESTION_TYPES))
    created_by = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    options = fields.Nested(QuestionOptionsSchema, required=True)


class QuizCategorySchema(CustomSchema):
    'Schema for Quiz Category data'

    category_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    category = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    created_by = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    question_data = fields.List(fields.Nested(QuizQuestionSchema), required=True)


class QuizDataSchema(CustomSchema):
    'Schema for Quiz data'

    quiz_data = fields.List(fields.Nested(QuizCategorySchema), required=True)


class QuestionUpdateSchema(CustomSchema):
    'Schema for updating a Question'

    question_text = fields.Str(required=True)


class QuestionParamSchema(CustomSchema):
    'Schema for query parameters in get quiz data'

    category_id = fields.Str(validate=validate.Regexp(RegexPattern.ID_PATTERN), required=False)


class QuizResponseSchema(ResponseSchema):
    'Schema for Quiz data response'
    
    data = fields.List(fields.Nested(QuizCategorySchema), required=True)

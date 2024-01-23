'Schema for Question data'

from marshmallow import Schema, fields, validate

from config.regex_patterns import RegexPattern


class QuestionSchema(Schema):
    'Schema for Question data'

    category_name = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    question_text = fields.Str(required=True, validate=validate.Regexp(RegexPattern.QUES_TEXT_PATTERN))
    question_type = fields.Str(required=True)
    answer = fields.Str(required=True, validate=validate.Regexp(RegexPattern.OPTION_TEXT_PATTERN))
    other_options = fields.List(fields.Str)


class QuestionOptionsSchema(Schema):
    'Schema for Options data'

    answer = fields.Str(required=True)
    other_options = fields.List(fields.Str(), missing=[])


class QuizQuestionSchema(Schema):
    'Schema for Quiz Question data'

    question_text = fields.Str(required=True)
    question_type = fields.Str(required=True)
    options = fields.Nested(QuestionOptionsSchema, required=True)


class QuizCategorySchema(Schema):
    'Schema for Quiz Category data'

    category = fields.Str(required=True)
    question_data = fields.List(fields.Nested(QuizQuestionSchema), required=True)


class QuizDataSchema(Schema):
    'Schema for Quiz data'

    quiz_data = fields.List(fields.Nested(QuizCategorySchema), required=True)


class QuestionUpdateSchema(Schema):
    'Schema for updating a Question'

    question_text = fields.Str(required=True)

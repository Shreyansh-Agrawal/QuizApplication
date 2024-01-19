'Schema for User data'

from marshmallow import Schema, fields, validate

from config.regex_patterns import RegexPattern


class UserSchema(Schema):
    'Schema for admin and player data'

    user_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    username = fields.Str(required=True, validate=validate.Regexp(RegexPattern.USERNAME_PATTERN))
    name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    email = fields.Str(required=True, validate=validate.Regexp(RegexPattern.EMAIL_PATTERN))
    registration_date = fields.Str(dump_only=True)

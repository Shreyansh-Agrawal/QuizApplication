'Schema for Auth data'

from marshmallow import Schema, fields, validate

from config.regex_patterns import RegexPattern



class LoginSchema(Schema):
    'Schema for login'

    username = fields.Str(required=True, validate=validate.Regexp(RegexPattern.USERNAME_PATTERN))
    password = fields.Str(required=True, load_only=True)


class RegistrationSchema(LoginSchema):
    'Schema for registration'

    name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    email = fields.Str(required=True, validate=validate.Regexp(RegexPattern.EMAIL_PATTERN))

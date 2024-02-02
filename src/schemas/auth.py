'Schema for Auth data'

from marshmallow import fields, validate

from config.regex_patterns import RegexPattern
from schemas.config_schema import CustomSchema, ResponseSchema


class LoginSchema(CustomSchema):
    'Schema for login'

    username = fields.Str(required=True, validate=validate.Regexp(RegexPattern.USERNAME_PATTERN))
    password = fields.Str(required=True, load_only=True)


class RegistrationSchema(LoginSchema):
    'Schema for registration'

    name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    email = fields.Str(required=True, validate=validate.Regexp(RegexPattern.EMAIL_PATTERN))


class LoginDataSchema(CustomSchema):
    'Schema for login data'

    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
    password_type = fields.Str(required=True)


class LoginResponseSchema(ResponseSchema):
    'Schema for login response'

    data = fields.Nested(LoginDataSchema)


class RefreshDataSchema(CustomSchema):
    'Schema for refresh endpoint data'

    access_token = fields.Str(required=True)


class RefreshResponseSchema(ResponseSchema):
    'Schema for refresh response'

    data = fields.Nested(RefreshDataSchema)

'Schema for User data'

from marshmallow import fields, validate

from config.regex_patterns import RegexPattern
from schemas.config_schema import CustomSchema, ResponseSchema


class UserSchema(CustomSchema):
    'Schema for admin and player data'

    user_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    username = fields.Str(required=True, validate=validate.Regexp(RegexPattern.USERNAME_PATTERN))
    name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    email = fields.Str(required=True, validate=validate.Regexp(RegexPattern.EMAIL_PATTERN))
    registration_date = fields.Str(dump_only=True)
    password = fields.Str(load_only=True)

class UserUpdateSchema(CustomSchema):
    'Schema for update profile'

    username = fields.Str(required=True, validate=validate.Regexp(RegexPattern.USERNAME_PATTERN))
    name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))
    email = fields.Str(required=True, validate=validate.Regexp(RegexPattern.EMAIL_PATTERN))

class PasswordUpdateSchema(CustomSchema):
    'Schema for update password'

    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


class ProfileResponseSchema(ResponseSchema):
    'Schema for view profile response'

    data = fields.Nested(UserSchema)


class UserResponseSchema(ProfileResponseSchema):
    'Schema for view users response'

    data = fields.Nested(UserSchema, many=True)

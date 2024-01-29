'Schema for Auth data'

from pydantic import BaseModel, Field

from config.regex_patterns import RegexPattern


class LoginSchema(BaseModel):
    'Schema for login'

    username: str = Field(pattern=RegexPattern.USERNAME_PATTERN)
    password: str = Field(min_length=6)


class RegistrationSchema(LoginSchema):
    'Schema for registration'

    name: str = Field(pattern=RegexPattern.NAME_PATTERN)
    email: str = Field(pattern=RegexPattern.EMAIL_PATTERN)

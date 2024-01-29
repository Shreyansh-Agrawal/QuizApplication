'Schema for User data'

from pydantic import BaseModel, Field

from config.regex_patterns import RegexPattern


class AdminSchema(BaseModel):
    'Schema for admin and player data'

    username: str = Field(pattern=RegexPattern.USERNAME_PATTERN)
    name: str = Field(pattern=RegexPattern.NAME_PATTERN)
    email: str = Field(pattern=RegexPattern.EMAIL_PATTERN)

class UserUpdateSchema(BaseModel):
    'Schema for update profile'

    username: str = Field(pattern=RegexPattern.USERNAME_PATTERN)
    name: str = Field(pattern=RegexPattern.NAME_PATTERN)
    email: str = Field(pattern=RegexPattern.EMAIL_PATTERN)
    password: str

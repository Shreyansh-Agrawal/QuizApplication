'Schema for Quiz data'

from pydantic import BaseModel, Field

from config.regex_patterns import RegexPattern


class AnswerSchema(BaseModel):
    'Schema for player answers'

    question_id: str = Field(pattern=RegexPattern.ID_PATTERN)
    user_answer: str = Field(pattern=RegexPattern.OPTION_TEXT_PATTERN)

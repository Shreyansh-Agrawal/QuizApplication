'Schema for Question data'

from typing import List

from pydantic import BaseModel, Field

from config.regex_patterns import RegexPattern


class QuestionSchema(BaseModel):
    'Schema for Question data'

    category_name: str = Field(pattern=RegexPattern.NAME_PATTERN)
    question_text: str = Field(pattern=RegexPattern.QUES_TEXT_PATTERN)
    question_type: str
    answer: str = Field(pattern=RegexPattern.OPTION_TEXT_PATTERN)
    other_options: List[str]


class QuestionOptionsSchema(BaseModel):
    'Schema for Options data'

    answer: str
    other_options: List = []


class QuizQuestionSchema(BaseModel):
    'Schema for Quiz Question data'

    question_text: str
    question_type: str
    options: QuestionOptionsSchema


class QuizCategorySchema(BaseModel):
    'Schema for Quiz Category data'

    category: str
    question_data: List[QuizQuestionSchema]


class QuizDataSchema(BaseModel):
    'Schema for Quiz data'

    quiz_data: List[QuizCategorySchema]


class QuestionUpdateSchema(BaseModel):
    'Schema for updating a Question'

    question_text: str

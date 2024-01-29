'Schema for Category data'

from pydantic import BaseModel, Field

from config.regex_patterns import RegexPattern


class CategorySchema(BaseModel):
    'Schema for Category data'

    category_name: str = Field(pattern=RegexPattern.NAME_PATTERN)


class CategoryUpdateSchema(BaseModel):
    'Schema for Category update data'

    updated_category_name: str = Field(pattern=RegexPattern.NAME_PATTERN)

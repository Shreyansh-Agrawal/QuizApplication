'Configurations for marshmallow schemas'

from marshmallow import Schema

from config.message_prompts import StatusCodes
from utils.custom_error import ValidationError


class CustomSchema(Schema):
    'Class to override default marshmallow validation error'

    def handle_error(self, error, data, many, **kwargs):
        'Method to override default marshmallow validation error'
        raise ValidationError(status=StatusCodes.UNPROCESSABLE_ENTITY, message=error)

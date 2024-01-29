'Success Message Dataclass'

from dataclasses import dataclass
from typing import Dict, NamedTuple


@dataclass
class SuccessMessage:
    'A custom success message class for successful response'

    status: NamedTuple
    message: str
    data: Dict = None

    @property
    def message_info(self):
        'Returns success message in json format'

        return {
            'code': self.status.code,
            'status': self.status.status,
            'message': self.message,
            'data': self.data
        }

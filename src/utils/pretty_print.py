'''Pretty print using tabulate library'''

import logging
from pprint import pprint
from typing import List, Tuple

from tabulate import tabulate

from config.message_prompts import DisplayMessage, LogMessage

logger = logging.getLogger(__name__)


def pretty_print(data: List[Tuple], headers: Tuple) -> None:
    '''
    Formats and displays data in a tabulated format using the tabulate library.

    Args:
        data (List[Tuple]): The data to be displayed as a table.
        headers (Tuple): Headers for the table.

    Returns:
        None
    '''
    row_id = list(range(1, len(data) + 1))
    headers = ('SNo.', *headers)

    try:
        print(tabulate(data, headers=headers, tablefmt='rounded_grid', showindex=row_id))
    except ValueError as e:
        logger.exception(LogMessage.TABULATE_ERROR, e)
        print(DisplayMessage.TABULATE_ERROR_MSG)
        pprint(data)

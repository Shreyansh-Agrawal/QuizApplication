'Contains logging configurations'

import logging
import os
from logtail import LogtailHandler
from config.flask_configs import CustomFilter


def set_log_configs():
    'Set custom configurations for logs'

    custom_formatter = logging.Formatter(
        # fmt='%(asctime)s %(levelname)-8s [%(request_id)s][%(filename)s:%(lineno)-d] %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )
    # custom_handler = logging.FileHandler("logs.log")
    custom_handler = LogtailHandler(source_token=os.getenv('LOG_TAIL_TOKEN'))
    custom_handler.setFormatter(custom_formatter)
    custom_handler.addFilter(CustomFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(custom_handler)

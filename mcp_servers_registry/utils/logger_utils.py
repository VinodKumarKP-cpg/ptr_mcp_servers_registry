import logging
import os
import tempfile
from logging.handlers import RotatingFileHandler


def get_logger():
    logger = logging.getLogger('root')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    temp_dir = tempfile.gettempdir()
    log_file_path = os.path.join(temp_dir, 'app.log')

    # Create a file handler to write logs to a file
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # You can set the desired log level for console output
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

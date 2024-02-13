import logging
import os
from datetime import datetime
import sys

class AppLogger:
    def __init__(self):
        self.log_directory = "logs"
        self.file_name = datetime.now().strftime("%Y-%m-%d") + ".log"
        self.create_log_directory()

        # Create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create file handler which logs even debug messages
        file_handler = logging.FileHandler(os.path.join(self.log_directory, self.file_name))
        file_handler.setLevel(logging.INFO)

        # Create console handler with a higher log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def create_log_directory(self):
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def log_info(self, message):
        """Logs an info message."""
        self.logger.info(message)

    def log_error(self, message):
        """Logs an error message."""
        self.logger.error(message)

    def log_warning(self, message):
        """Logs a warning message."""
        self.logger.warning(message)

    def log_exception(self, message):
        """Logs an exception message."""
        self.logger.exception(message)

# Example Usage
if __name__ == "__main__":
    logger = AppLogger()
    logger.log_info("This is an info message")
    try:
        1 / 0
    except Exception as e:
        logger.log_exception("Exception occurred")

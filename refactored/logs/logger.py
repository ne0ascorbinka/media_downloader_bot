"""
logger module contains logger object
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import sys
import os, os.path
from config.config import config

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='midnight'):
        self._original_filename = filename
        super().__init__(filename, when=when)

    # change file name in format %Y-%m-%d.log
    def rotation_filename(self, default_name):
        return os.path.join(config.logs_path, str(datetime.date.today() - datetime.timedelta(days=1)) + ".log")

class LoggerConfigurator:
    @staticmethod
    def configure_logger(logger: logging.Logger):
        if not os.path.exists(config.logs_path):
            os.mkdir(config.logs_path)
        
        logger.setLevel(logging.INFO)

        # Create custom timed rotating file handler
        log_filename = os.path.join(config.logs_path, "temp.log")
        file_handler = CustomTimedRotatingFileHandler(log_filename)
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setLevel(logging.INFO)

        # Create formatter and add to file handler
        formatter = logging.Formatter(fmt="[{asctime}] - [{levelname}] - user{id} - {query} - {message}",
                                        datefmt="%H-%M-%S", style='{')

        # formatter = logging.Formatter(fmt="[{asctime}] - [{levelname}] - user###### - {funcName} - {message}",
        #                                   datefmt="%Y-%m-%d", style='{')

        file_handler.setFormatter(formatter)

        # Add file handler to logger
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


# Create logger
logger = logging.getLogger(__name__)
LoggerConfigurator.configure_logger(logger)
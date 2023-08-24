"""
logger module contains logger object and useless stupid ass nigga Status enum that I've 
added because I'm stupid and now it should be contained in extra in every logger message (sorry guys)
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import sys
import os, os.path
from enum import Enum
from config.config import config

class Status(Enum):
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    UNKNOWN = "UNKNOWN"

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename):
        self._original_filename = filename
        super().__init__(filename, when='midnight')

    # change file name in format %Y-%m-%d.log
    def rotation_filename(self, default_name):
        return os.path.join(config.logs_path, str(datetime.date.today() - datetime.timedelta(days=1)) + ".log")

if not os.path.exists(config.logs_path):
    os.mkdir(config.logs_path)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create custom timed rotating file handler
log_filename = os.path.join(config.logs_path, "temp.log")
file_handler = CustomTimedRotatingFileHandler(log_filename)
file_handler.suffix = "%Y-%m-%d.log"
file_handler.setLevel(logging.INFO)

# Create formatter and add to file handler
# formatter = logging.Formatter(fmt="[{asctime}] - [{levelname}] - user{id} - {funcName} - {message}",
#                                   datefmt="%Y-%m-%d", style='{')
formatter = logging.Formatter(fmt="[{asctime}] - [{levelname}] -  {funcName} - {message}",
                                  datefmt="%Y-%m-%d", style='{')
# formatter = logging.Formatter(fmt="[{asctime}] - [{levelname}] - user{id} - {query} - {message} - {status.value}",
#                                   datefmt="%Y-%m-%d", style='{',
#                                   defaults={"id" : "######",
#                                             "query" : "funcName",
#                                             "status" : Status.UNKNOWN}) #defaults are available only from python3.10 :(

# formatter = logging.Formatter(fmt="[{asctime}] - [{levelname}] - user###### - {funcName} - {message} - UNKNOWN",
#                                   datefmt="%Y-%m-%d", style='{')

file_handler.setFormatter(formatter)

# Add file handler to logger
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# debug_handler = logging.StreamHandler(sys.stdout)
# debug_handler.setLevel(logging.DEBUG)
# debug_handler.setFormatter(formatter)
# logger.addHandler(formatter)
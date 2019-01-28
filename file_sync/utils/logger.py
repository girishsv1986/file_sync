"""
# This file contains all logging utilities.
"""

import os.path
import logging
from logging.handlers import TimedRotatingFileHandler
from file_sync import FLASK_APP

# Mapping for logging levels
LOG_LEVELS = {
  "DEBUG": logging.DEBUG,
  "INFO": logging.INFO,
  "WARNING": logging.WARNING,
  "ERROR": logging.ERROR,
  "CRITICAL": logging.CRITICAL
}

def get_logger(name):
  """
  Returns a logger object initialized with a file handler
  and a pre-defined log format

  Args:
    name(str): Name of the logger

  Returns:
    (logger object): A logger object
  """
  filename = "file_sync.log"
  _create_log_dir()
  filepath = os.path.join(FLASK_APP.config["LOG_DIR"], filename)
  logger = logging.getLogger(name)
  handler = TimedRotatingFileHandler(filepath, when="midnight")
  logger.setLevel(LOG_LEVELS[FLASK_APP.config["LOG_LEVEL"]])
  handler.setLevel(LOG_LEVELS[FLASK_APP.config["LOG_LEVEL"]])
  log_format = ("%(asctime)s %(levelname)s %(pathname)s"
                ":%(funcName)s: %(lineno)d - %(message)s")
  formatter = logging.Formatter(log_format)
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger

def _create_log_dir():
  """
    creates log directory is not exists
  """
  if not os.path.exists(FLASK_APP.config["LOG_DIR"]):
    os.makedirs(FLASK_APP.config["LOG_DIR"])

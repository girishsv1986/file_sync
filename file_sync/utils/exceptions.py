"""
  Application specific exception classes and error codes
"""

UNKNOWN_ERROR = 1000

MISSING_REQUIRED_INPUT = 1001
INVALID_INPUT = 1002
ALREADY_EXISTS = 1003
INVALID_TOKEN = 1004

class DataValidationException(Exception):
  """
    Exception class for data validation error
  """
  pass

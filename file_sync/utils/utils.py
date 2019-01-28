"""
"""
import os
import random
from string import ascii_uppercase, digits, ascii_lowercase

from file_sync.models.model import Files
from file_sync import FLASK_APP

CHOICES = ascii_lowercase + ascii_uppercase + digits

def generate_token(length=10):
  """
    returns a randomly generated token
  """
  return "".join(random.choice(CHOICES) for _ in range(length))

def get_file_path(name):
  """
    returns file storage path on server file system
  """
  return os.path.join(FLASK_APP.config["COMMON_STORAGE_LOCATION"], name)

def generate_sql_alchemy_filter_format(filters):
  """
    Construct filters for the file object which can be used in ORM queries.
  """
  filter_flds = {
    "file_name" : Files.file_name,
    "user_name" : Files.user_name,
    "token": Files.token
    }

  filter_on_fields = []
  for fld, value in filters:
    if fld in filter_flds:
      filter_on_fields.append((filter_flds[fld] == value))

  return filter_on_fields

"""
  Application specific model and serializer classes
"""
from datetime import datetime

from sqlalchemy.orm import validates

from file_sync import DB, MA
from file_sync.utils import exceptions

MAX_STRING_LENGTH = 64
class Files(DB.Model):
  """
    File information model class
  """
  id = DB.Column(DB.Integer, primary_key=True)
  file_name = DB.Column(
    DB.String(MAX_STRING_LENGTH), unique=False, nullable=False)
  #If we need to store additional information for user, the this can be
  #  normalized to have a separate user table
  user_name = DB.Column(
    DB.String(MAX_STRING_LENGTH), unique=False, nullable=False)
  token = DB.Column(
    DB.String(MAX_STRING_LENGTH), unique=True, nullable=False)
  file_path = DB.Column(
    DB.String(MAX_STRING_LENGTH*4), unique=True, nullable=False)
  created = DB.Column(DB.DateTime(), nullable=False)
  DB.UniqueConstraint('file_name', 'user_name', name='user_name_file_name_idx')

  @validates("token")
  def validate_token(self, _, token):
    """
      Validate token properties
    """
    if not token:
      raise exceptions.DataValidationException("token can't be empty")

    if len(token) > MAX_STRING_LENGTH:
      raise exceptions.DataValidationException("Invalid length of token")
    return token

  @validates("user_name")
  def validate_user_name(self, _, user_name):
    """
      Validate user_name properties
    """
    if not user_name:
      raise exceptions.DataValidationException("user_name can't be empty")

    if len(user_name) > MAX_STRING_LENGTH:
      raise exceptions.DataValidationException(
        "Invalid length of user_name name")
    return user_name

  @validates("file_name")
  def validate_file_name(self, _, file_name):
    """
      Validate file_name properties
    """
    if not file_name:
      raise exceptions.DataValidationException("file_name can't be empty")

    if len(file_name) > MAX_STRING_LENGTH:
      raise exceptions.DataValidationException("Invalid length of file name")
    return file_name

  def __init__(self, file_name, user_name, token=None, file_path=None):
    self.file_name = file_name
    self.user_name = user_name
    self.token = token
    self.file_path = file_path
    self.created = datetime.utcnow()

# Model serializer

class FileSchema(MA.Schema):
  """
    Serializer for models.User class
  """
  class Meta:
    """
      metadata class
    """
    # Fields to expose
    fields = ("file_name", "user_name", "token", "created")

file_schema = FileSchema()
files_schema = FileSchema(many=True)

"""
  Helper module to perform ORM queries for parking slots related operations
"""
from multiprocessing import Lock
import codecs

from sqlalchemy import and_

from file_sync.models.model import Files
from file_sync.utils import utils, logger, exceptions
from file_sync import DB

LOG = logger.get_logger(__name__)

LOCK = Lock()

def add_new_file(fields):
  """
    Create a new file entry with user name and token
  """
  filters = (("file_name", fields["file_name"]),
             ("user_name", fields["user_name"]))
  new_file_obj = None
  with DB.session.begin():
    existing_object = get_files_by_filter((filters))
    if existing_object:
      raise exceptions.DataValidationException(
        "Record with given file_name and user_name already exists")

    fields["token"] = utils.generate_token()
    fields["file_path"] = utils.get_file_path("%s_%s" % (
      fields["file_name"], fields["user_name"]))
    new_file_obj = Files(**fields)

    DB.session.add(new_file_obj)
  return new_file_obj

def get_file_by_id(file_id):
  """
    Get file information for a given id
  """
  return Files.query.get(file_id)

def get_files_by_filter(filters=None):
  """
    Get the list of files for given filters if any
  """
  if not filters:
    return Files.query.all()

  filter_on_fields = utils.generate_sql_alchemy_filter_format(filters)

  return DB.session.query(Files).filter(and_(*filter_on_fields)).all()

def get_file_content(token):
  """
  Get the file content for a given token. Function first validates token is
    valid and return the content of the file.
  Args:
    token(str): token value for which content to be retrieved.

  Returns: Content of the file identified by the token
  """
  filters = (("token", token),)
  file_record = None
  with DB.session.begin():
    file_record = get_files_by_filter((filters))

    if not file_record:
      raise exceptions.DataValidationException(
        "No record exists with token '%s'" % token)
    file_record = file_record[0]

  try:
    with codecs.open(
      file_record.file_path, "r", encoding="utf-8") as file_handle:
      return file_handle.read()
  except OSError as oe:
    LOG.error("Error occurred for updating content", exc_info=True)
    raise oe
  except IOError:
    # File entry exists, but file not created yet
    LOG.warning("File '%s' not created yet")
    return ""

def add_content_to_file(token, contents):
  """
  Append the content to file for a given token. Function first validates token
    is valid and append the content to the file.
  Args:
    token(str): token value for which content to be added.
    contents(str): contents to append to the file.

  Returns: Boolean status True or False
  """
  filters = (("token", token),)
  file_record = None
  with DB.session.begin():
    file_record = get_files_by_filter((filters))

    if not file_record:
      raise exceptions.DataValidationException(
        "No record exists with token '%s'" % token)
    file_record = file_record[0]

  try:
    LOCK.acquire()
    if contents:
      with codecs.open(
        file_record.file_path, "a", encoding="utf-8") as file_handle:
        file_handle.write(contents)

  except OSError:
    LOG.error("Error occurred for updating content", exc_info=True)
    return False
  finally:
    LOCK.release()
  return True

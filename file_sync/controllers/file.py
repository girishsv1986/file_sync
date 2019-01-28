"""
  REST end points related to files entity
"""
from flask import Blueprint, request, jsonify, json, Response
from file_sync.models.model import file_schema, files_schema
from file_sync.models import api
from file_sync.utils import logger
from file_sync.utils import exceptions

LOG = logger.get_logger(__name__)

file_routes = Blueprint("file", __name__, url_prefix="")

# endpoint to create new file entry
@file_routes.route("/file", methods=["POST"])
def add_new_file():
  """
    Rest point to create new file to sync
  """
  try:
    file_name = request.json["file_name"]
    user_name = request.json["user_name"]
  except KeyError as ke:
    return Response(
      response=json.dumps({"error": "Missing required input %s" % ke,
                           "error_code": exceptions.MISSING_REQUIRED_INPUT}),
      status=500,
      mimetype='application/json')
  except Exception as ex:
    LOG.error("Error getting payload for create file entry", exc_info=True)
    return Response(
      response=json.dumps({"error": "Invalid Input",
                           "error_code": exceptions.INVALID_INPUT}),
      status=500,
      mimetype='application/json')

  try:
    file_object = api.add_new_file({"file_name": file_name,
                                    "user_name": user_name})
  except exceptions.DataValidationException as dve:
    LOG.error(
      "Data validation error creating new file entry", exc_info=True)
    return Response(
      response=json.dumps({"error": dve.message,
                           "error_code": exceptions.ALREADY_EXISTS}),
      status=500,
      mimetype='application/json')
  except Exception as ex:
    LOG.error("Error creating new file entry", exc_info=True)
    return Response(
      response=json.dumps({"error": ex.message,
                           "error_code": exceptions.UNKNOWN_ERROR}),
      status=500,
      mimetype='application/json')

  return file_schema.jsonify(file_object)

# endpoint to show all files sync entries
# This API can be further enhanced to support pagination
@file_routes.route("/files", methods=["GET"])
def get_all_files():
  """
    Rest point to return all files entries
  """
  filters = []
  if "file_name" in request.args:
    filters.append(("file_name", request.args["file_name"]),)
  elif "user_name" in request.args:
    filters.append(("user_name", request.args["user_name"]),)


  try:
    result = files_schema.dump(api.get_files_by_filter(filters))
  except Exception as ex:
    LOG.error(
      "Error creating new file entry", exc_info=True)
    return Response(
      response=json.dumps({"error": ex.message,
                           "error_code": exceptions.UNKNOWN_ERROR}),
      status=500,
      mimetype='application/json')
  return jsonify(result.data)

# Add file contents
@file_routes.route("/file/content/<token>", methods=["PATCH"])
def sync_file_contents(token):
  """
    Rest point to sync file content from client to server
  """
  try:
    content = request.json["contents"]
    # Validating content assuming only append is allowed, not replacing the
    # content of files to make it empty
    if not content:
      raise exceptions.DataValidationException("Nothing to append to file")
  except exceptions.DataValidationException as dve:
    return Response(
      response=json.dumps({"error": dve.message,
                           "error_code": exceptions.INVALID_INPUT}),
      status=500,
      mimetype='application/json')
  except KeyError as ke:
    return Response(
      response=json.dumps({"error": "Missing required input %s" % ke,
                           "error_code": exceptions.MISSING_REQUIRED_INPUT}),
      status=500,
      mimetype='application/json')
  except Exception as ex:
    return Response(
      response=json.dumps({"error": "Invalid Input",
                           "error_code": exceptions.INVALID_INPUT}),
      status=500,
      mimetype='application/json')

  try:
    status = api.add_content_to_file(token, content)
  except exceptions.DataValidationException as dve:
    return Response(
      response=json.dumps({"error": dve.message,
                           "error_code": exceptions.INVALID_TOKEN}),
      status=500,
      mimetype='application/json')
  except Exception as ex:
    LOG.error("Error occurred for syncing file contents: %s" % str(ex),
              exc_info=True)
    return Response(
      response=json.dumps({"error": "Unknown error occurred.",
                           "error_code": exceptions.UNKNOWN_ERROR}),
      status=500,
      mimetype='application/json')

  return Response(response=json.dumps({"status": status}),
                  mimetype='application/json')

@file_routes.route("/file/content/<token>", methods=["GET"])
def get_file_content(token):
  """
    Rest point to return file content using file token
  """
  try:
    contents = api.get_file_content(token)
  except exceptions.DataValidationException as dve:
    return Response(
      response=json.dumps({"error": dve.message,
                           "error_code": exceptions.INVALID_TOKEN}),
      status=500,
      mimetype='application/json')
  except Exception as ex:
    LOG.error("Error occurred for syncing file contents: %s" % str(ex),
              exc_info=True)
    return Response(
      response=json.dumps({"error": "Unknown error occurred.",
                           "error_code": exceptions.UNKNOWN_ERROR}),
      status=500,
      mimetype='application/json')
  return Response(response=json.dumps({"contents": contents}),
                  mimetype='application/json')

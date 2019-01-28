"""
  Unit test to test REST api end points
"""

import unittest
import os
import json
from file_sync import FLASK_APP, DB

BASE_URL = "http://127.0.0.1:8080/"

class BucketlistTestCase(unittest.TestCase):
  """
    This class represents the file_sync API test case
  """
  def setUp(self):
    """
      Test variables and app initialization
    """
    self.app = FLASK_APP
    self.app_url = BASE_URL

    self.client = self.app.test_client

    self.file_name = "some_file"
    self.user_name = "some_user"

    # binds the app to the current context
    with self.app.app_context():
      DB.create_all()

  def tearDown(self):
    """
    teardown all initialized variables.
    """
    with self.app.app_context():
      DB.session.remove()
      DB.drop_all()
      try:
        os.remove(
          os.path.join(FLASK_APP.config["COMMON_STORAGE_LOCATION"],
                       "%s_%s" % (self.file_name, self.user_name)))
      except OSError:
        pass

  def test_add_new_file_entry_invalid_input(self):
    """
    Test API response for new file entry when invalid request is made, say
    unexpected content type
    """
    res = self.client().post('/file',
                             data=json.dumps({"user_name": self.user_name}))

    error_dict = {"error": "Invalid Input",
                  "error_code": 1002}

    self.assertEqual(res.status_code, 500)
    self.assertDictEqual(error_dict, res.json)

  def test_add_new_file_entry_success(self):
    """
      Test API can create a new file entry to be synced
      using a post request
    """
    res = self.client().post('/file',
                             data=json.dumps({"user_name": self.user_name,
                                              "file_name": self.file_name}),
                             content_type="application/json")
    self.assertEqual(res.status_code, 200)
    self.assertIn("token", res.data)

  def test_add_new_file_entry_missing_file_name(self):
    """
    Test API response for new file entry when file_name missing in payload
    """
    res = self.client().post('/file',
                             data=json.dumps({"user_name": self.user_name}),
                             content_type="application/json")

    error_dict = {"error": "Missing required input 'file_name'",
                  "error_code": 1001}

    self.assertEqual(res.status_code, 500)
    self.assertDictEqual(error_dict, res.json)

  def test_add_new_file_entry_missing_user_name(self):
    """
    Test API response for new file entry when user_name missing in payload
    """
    res = self.client().post('/file',
                             data=json.dumps({"file_name": self.file_name}),
                             content_type="application/json")

    error_dict = {"error": "Missing required input 'user_name'",
                  "error_code": 1001}

    self.assertEqual(res.status_code, 500)
    self.assertDictEqual(error_dict, res.json)

  def test_get_file_content_invalid_token(self):
    """
    Test API response for get file content  file entry when invalid token
    is provided
    """
    res = self.client().get('/file/content/invalid_token',
                            content_type="application/json")

    error_dict = {"error": "No record exists with token 'invalid_token'",
                  "error_code": 1004}

    self.assertEqual(res.status_code, 500)
    self.assertDictEqual(error_dict, res.json)

  def test_get_file_content_valid_token_response(self):
    """
    Test API response for get file content file entry when a valid token
    is provided
    """
    res = self.client().post('/file',
                             data=json.dumps({"user_name": self.user_name,
                                              "file_name": self.file_name}),
                             content_type="application/json")

    res = self.client().get('/file/content/%s' % res.json["token"],
                            content_type="application/json")

    self.assertEqual(res.status_code, 200)
    self.assertIn("contents", res.json)

  def test_sync_file_content_invalid_token(self):
    """
    Test API response for sync file content invalid token
    is provided
    """
    res = self.client().patch('/file/content/invalid_token',
                              data=json.dumps({"contents": "some_content"}),
                              content_type="application/json")

    error_dict = {"error": "No record exists with token 'invalid_token'",
                  "error_code": 1004}

    self.assertEqual(res.status_code, 500)
    self.assertDictEqual(error_dict, res.json)

  def test_sync_file_content_valid_token_response(self):
    """
    Test API response for sync file content when a valid token
    is provided
    """
    res = self.client().post('/file',
                             data=json.dumps({"user_name": self.user_name,
                                              "file_name": self.file_name}),
                             content_type="application/json")

    res = self.client().patch('/file/content/%s' % res.json["token"],
                              data=json.dumps({"contents": "some_content"}),
                              content_type="application/json")

    expected_response = {"status": True}
    self.assertEqual(res.status_code, 200)
    self.assertDictEqual(expected_response, res.json)

  def test_sync_file_content_get_response(self):
    """
    Test synced file content getting appended to the file
    """
    res = self.client().post('/file',
                             data=json.dumps({"user_name": self.user_name,
                                              "file_name": self.file_name}),
                             content_type="application/json")

    token = res.json["token"]
    res = self.client().patch('/file/content/%s' % token,
                              data=json.dumps({"contents": "some_content"}),
                              content_type="application/json")

    res = self.client().get('/file/content/%s' % token,
                            content_type="application/json")

    expected_response = {"contents": "some_content"}
    self.assertEqual(res.status_code, 200)
    self.assertDictEqual(expected_response, res.json)

if __name__ == "__main__":
  unittest.main()

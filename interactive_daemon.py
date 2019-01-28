"""
Command line utility to synchronize file content using file tokens
as identifier
"""
import json

import requests

APPLICATION_HOST = "http://10.4.96.190:8080"
FILE_SYNC_URL = "/file/content/%s"

def get_file_content(token):
  """
    Helper method to get the file contents from server
  """
  session = requests.Session()
  session.headers.update(
    {'Content-Type': 'application/json; charset=utf-8'})

  try:
    return session.get(
      "%s%s" % (APPLICATION_HOST, FILE_SYNC_URL % token)).json()
  except requests.exceptions.ConnectionError as ce:
    return "Error: %s" % str(ce)
  except requests.exceptions.Timeout as to:
    return "Error: %s" % str(to)
  except Exception as ex:
    return "Error: %s" % str(ex)

def upload_file_content(token, content):
  """
    Helper method to upload file contents to server
  """
  session = requests.Session()
  session.headers.update(
    {'Content-Type': 'application/json; charset=utf-8'})

  try:
    return session.post(
      "%s%s" % (APPLICATION_HOST, FILE_SYNC_URL % token),
      data=json.dumps({"contents": "%s\n" % content})).json()
  except requests.exceptions.ConnectionError as ce:
    return "Error: %s" % str(ce)
  except requests.exceptions.Timeout as to:
    return "Error: %s" % str(to)
  except Exception as ex:
    return "Error: %s" % str(ex)

def is_valid_token(token):
  """
    Helper method to validate given token is valid or not
  """
  content = get_file_content(token)
  return "contents" in content

def show_main_menu():
  """
    Helper method to print main menu
  """
  print "----------FILE OPERATIONS MENU----------"
  print "1. File operations"
  print "2. Exit"

def file_sync_menu():
  """
    Helper method to print menu for file sync and perform required operations
  """
  token = raw_input("Enter file token: ")

  print "Validating file token ..."
  if not is_valid_token(token):
    print "\n\nInvalid file token.\n\n"
    return
  print "Validated file token"

  while True:
    print "----------FILE SYNC MENU----------"
    print "1. Get file content"
    print "2. Write content to file"
    print "3. Back to main menu"

    choice = raw_input("Enter your choice: ")

    try:
      choice = int(choice)
    except ValueError:
      print "Invalid input"
      continue

    if int(choice) not in [1, 2, 3]:
      print "Invalid choice"
      continue

    if choice == 3:
      break
    elif choice == 1:
      print "----------BEGIN FILE CONTENT----------"
      print get_file_content(token)["contents"]
      print "----------END FILE CONTENT----------"
    elif choice == 2:
      content = raw_input("Enter file content to sync\n")
      if content.strip():
        result = upload_file_content(token, content)
        if result["status"]:
          print "Content synced successfully."
        else:
          print "Failed to sync file content, check server logs for errors."

if __name__ == "__main__":
  while True:
    show_main_menu()
    choice = raw_input("Enter your choice: ")

    try:
      choice = int(choice)
    except ValueError:
      print "Invalid input"
      continue

    if int(choice) not in [1, 2]:
      print "Invalid choice"
      continue

    choice = int(choice)

    if choice == 2:
      break
    elif choice == 1:
      file_sync_menu()

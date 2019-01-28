"""
  Application related configuration
"""
# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Log directory location
LOG_DIR = os.path.join(BASE_DIR, "logs/")

LOG_LEVEL = "DEBUG"

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'file_sync.db')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED = True

CSRF_SESSION_KEY = "secret"

COMMON_STORAGE_LOCATION = os.path.join(BASE_DIR, "file_store")

if not os.path.exists(COMMON_STORAGE_LOCATION):
  os.makedirs(COMMON_STORAGE_LOCATION)
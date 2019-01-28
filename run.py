"""
  Run application server in development mode
"""
from file_sync import FLASK_APP
FLASK_APP.run(host='0.0.0.0', port=8080, debug=True)
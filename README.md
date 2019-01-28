# file_sync

Assumptions
1. Only single client/daemon will upload/sync file content
2. Parallel file content update/sync for the same file, may not work perfectly or can change the order
of file contents
3. Application user has write permission to create/write files.

To Run - 
1. Create a virtual environment and install the required dependencies from requirement.txt
2. To run web server from terminal - python run.py
3. To run interactive file daemon - python interactive_daemon.py

-- Use /file POST api to create new file entry to be sync on server
	with payload {"file_name": <file_name>,
				  "user_name": <user_name>}
-- Use /files GET api to get list of all files info including their token
-- Use /file/content/<token> GET api to get file content for given token
-- Use /file/content/<token> PATCH api to get sync file content for given token
	with payload {"contents": <content_to_sync>}

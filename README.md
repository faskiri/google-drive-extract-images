google-drive-extract-images
===========================

Extracts images from google drive using Google Drive APIs

The code is super simple and does not intend to handle any corner cases. It was really a single use thing that I have saved to github. Feel free to use as a sample tool to see how google api is used. Among other missing things, I have been lazy enough to not have implemented a proper CLI to ask for cliend id etc. To use, you have to open the file and modify the following:

CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
folder_id = 'folder-id'

Google API enabling
-------------------
From https://developers.google.com/drive/web/quickstart/quickstart-python#step_1_enable_the_drive_api
1. Go to the Google Developers Console.
2. Select a project, or create a new one.
3. In the sidebar on the left, expand APIs & auth. Next, click APIs. In the list of APIs, make sure the status is ON for the Drive API.
4. In the sidebar on the left, select Credentials.


#!/usr/bin/python
import argparse
import httplib2
import os
import pprint
import StringIO
import zipfile

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient import errors
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools

# Copy your credentials from the console
folder_id = 'folder-id'
folder_id = '0B__2OhShVLfSSUpvX1hlSUR5SW8'
CLIENT_ID = '1078892468156-lk6kdudv026jppopcaudaitos07rddku.apps.googleusercontent.com'
CLIENT_SECRET = 'RFn4cV4Bi1PyTh1qEnrUcgJW'

def get_credentials(path):
  storage = Storage(path)
  if os.path.exists(path):
    return storage.get()

  # Check https://developers.google.com/drive/scopes for all available scopes
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive.readonly'

  # Redirect URI for installed apps
  REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

  # Run through the OAuth flow and retrieve credentials
  flow = OAuth2WebServerFlow(
      CLIENT_ID,
      CLIENT_SECRET,
      OAUTH_SCOPE,
      redirect_uri=REDIRECT_URI)

  parser = argparse.ArgumentParser(parents=[tools.argparser])
  flags = parser.parse_args()
  credentials = tools.run_flow(flow, storage, flags)
  storage.put(credentials)
  return credentials

credentials = get_credentials('credentials.db')

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

page_token = None
while True:
  try:
    param = {}
    if page_token:
      param['pageToken'] = page_token
    children = drive_service.children().list(
        folderId=folder_id, **param).execute()

    for child in children.get('items', []):
      file = drive_service.files().get(fileId=child['id']).execute()
      print 'Downloading title: %s' % file['title']
      links = file.get('exportLinks')
      if links:
        openxml = links.get('application/vnd.openxmlformats-officedocument.presentationml.presentation')
        if openxml:
          resp, content = drive_service._http.request(openxml)
          if resp.status == 200:
            if not os.path.exists('media'): os.mkdir('media')
            ppt_dir = os.path.join('media',
                file['title'].replace(' ', '_'))

            base_dir = ppt_dir
            for i in range(100):
              if not os.path.exists(ppt_dir):
                break
              ppt_dir = base_dir + '_' + str(i)
            os.mkdir(ppt_dir)

            with zipfile.ZipFile(StringIO.StringIO(content)) as z:
              for name in z.namelist():
                if 'media' in name or '.xml.rels' in name or '*.xml' in name:
                  with z.open(name) as zi, open('%s/%s' % (ppt_dir,
                      os.path.basename(name)), 'w') as media:
                    media.write(zi.read())

    page_token = children.get('nextPageToken')
    if not page_token:
      break
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    break

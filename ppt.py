#!/usr/bin/python
import os
import pprint
import StringIO
import zipfile

import credentials

from apiclient.discovery import build
from apiclient import errors

# Copy your credentials from the console
folder_id = 'folder-id'
folder_id = '0B__2OhShVLfSSUpvX1hlSUR5SW8'

http = credentials.Authorizor().new_http_instance()
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
            if not os.path.exists('ppt'): os.mkdir('ppt')
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
                if 'media' in name or '.xml.rels' in name or '.xml' in name:
                  with z.open(name) as zi, open('%s/%s' % (ppt_dir,
                      os.path.basename(name)), 'w') as media:
                    media.write(zi.read())

    page_token = children.get('nextPageToken')
    if not page_token:
      break
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    break

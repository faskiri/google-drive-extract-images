#!/usr/bin/python
import collections
import csv
import httplib2
import os
import re
import StringIO
import sys

from apiclient.discovery import build
from apiclient import errors

import credentials
import model

Row = collections.namedtuple(
  'Row',
  'module_owner,module,text,image_file_name,image_remote_url,usage_sentence')

if len(sys.argv) != 2:
  print "Usage: python %s <url of the sheet>" % __file__
  sys.exit(1)

id_gid_re = re.compile('.*/spreadsheets/d/([^/]*)/.*#gid=(.*)')
m = id_gid_re.match(sys.argv[1])
if m is None:
  print "Please make sure you enter the URL of the sheet which is of the form" \
      "..../spreadsheets/d/13eDmNUa7qrb0sRE8DqGOJ0lNofw2I5gnsDIx7O8j1eA/...#gid=1223708539"
  sys.exit(1)

http = credentials.Authorizor().new_http_instance()
service = build('drive', 'v2', http=http)
id, gid = m.groups()
metadata = service.files().get(fileId=id, fields='exportLinks').execute()
url = metadata['exportLinks']['text/csv'] + '&gid=' + gid
resp, content = http.request(url)

modules = {}
if resp.status == 200:
  reader =  csv.reader(StringIO.StringIO(content))
  for cols in reader:
    row = Row._make(cols)
    m = modules.get(row.module, model.Model(row.module))
    m.add_object(text=row.text, image=row.image_file_name)
    modules[row.module] = m

  for m in modules.values():
    m.write()
else:
  print "Please check the URL got ", resp

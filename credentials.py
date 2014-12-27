import argparse
import httplib2
import os

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools

class Authorizor(object):
  def __init__(self):
    self._path = 'credentials.db'

  def new_http_instance(self):
    credentials = self._get_credentials()

    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    return credentials.authorize(http)

  def _get_credentials(self):
    path = self._path
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

import os

from django.core.management import CommandError
from dropbox import Dropbox, exceptions


class DropboxHelper(object):

    def __init__(self, access_token):
        self.dropbox = Dropbox(oauth2_access_token=access_token)

    def upload(self, file_path):
        with open(file_path, 'rb') as f:
            try:
                self.dropbox.files_upload(f.read(), '/' + file_path)
            except exceptions.BadInputError:
                os.remove(file_path)
                raise CommandError('Unable to upload file to Dropbox. Maybe access token is invalid.')
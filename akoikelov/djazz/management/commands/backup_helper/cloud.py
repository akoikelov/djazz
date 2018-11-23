import os

from django.core.management import CommandError
from dropbox import Dropbox


class DropboxHelper(object):

    def __init__(self, access_token):
        self.dropbox = Dropbox(oauth2_access_token=access_token)

    def upload(self, filename, file_path):
        with open(file_path, 'rb') as f:
            try:
                self.dropbox.files_upload(f.read(), '/' + filename)
            except Exception:
                os.remove(file_path)
                raise CommandError('Unable to upload file to Dropbox. Maybe access token is invalid.')

    def delete_all_files(self):
        for i in self.dropbox.files_list_folder('').entries:
            self.dropbox.files_delete(i.path_lower)

    def download_last_backup(self, dir_path):
        entries = self.dropbox.files_list_folder('').entries

        if len(entries) == 0:
            raise CommandError('We could not find any backup.')

        entry = entries[-1]
        full_path = dir_path + entry.path_lower

        self.dropbox.files_download_to_file(full_path, entry.path_lower)
        return full_path, entry.content_hash
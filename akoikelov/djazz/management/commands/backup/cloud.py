from dropbox import Dropbox


class DropboxHelper(object):

    def __init__(self, access_token):
        self.dropbox = Dropbox(oauth2_access_token=access_token)
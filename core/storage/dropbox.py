from os import path

from dropbox import dropbox

from core.utils import log_upload, log_download


class DropboxStorage:
    def __init__(self, index, token):
        self.index = index
        self.dbx = dropbox.Dropbox(token)
        self.name = 'dropbox'

    @log_upload
    def upload(self, filepath):
        with open(filepath, "rb") as f:
            self.dbx.files_upload(f.read(), path.basename(filepath), mode=dropbox.files.WriteMode.overwrite)

    @log_download
    def download(self, filename, target_dir=''):
        download_path = path.join(target_dir, filename)
        self.dbx.files_download_to_file(download_path=download_path, path=filename)

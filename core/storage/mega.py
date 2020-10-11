from datetime import datetime
import os

from mega import Mega

from core.utils import log_upload, log_download


class MegaStorage:
    def __init__(self, index, username, password):
        self.index = index
        self.mega = Mega()
        self.name = 'mega'
        self.mega.login(username, password)

    @log_upload
    def upload(self, filepath):
        self.mega.upload(filepath)

        return os.path.basename(filepath)

    @log_download
    def download(self, filename, target_dir=''):
        file = self.mega.find(filename)
        self.mega.download(file, target_dir)

        return os.path.join(target_dir, filename)

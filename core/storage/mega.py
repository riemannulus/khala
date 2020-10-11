from datetime import datetime
import os

from mega import Mega


class MegaStorage:
    def __init__(self, index, username, password):
        self.index = index
        self.username = username
        self.password = password
        self.name = 'mega'

    def upload(self, filepath):
        mega = Mega()
        print(f"[{datetime.now()}] upload start: {filepath}")

        mega.login(self.username, self.password)
        mega.upload(filepath)

        print(f"[{datetime.now()}] uploaded: {filepath}")

        return os.path.basename(filepath)

    def download(self, filename, target_dir=''):
        mega = Mega()
        print(f"[{datetime.now()}] download start: {filename}")

        mega.login(self.username, self.password)
        file = mega.find(filename)
        mega.download(file, target_dir)

        print(f"[{datetime.now()}] downloaded: {filename}")

        return os.path.join(target_dir, filename)

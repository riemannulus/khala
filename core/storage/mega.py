from datetime import datetime
import os

from mega import Mega

from core.utils import log_upload, log_download, get_latest_account_index

class MegaStorage:
    def __init__(self, index, username, password):
        self.index = index
        self.mega = Mega()
        self.name = 'mega'
        self.username = username
        self.password = password
        self.mega.login(username, password)

    @log_upload
    def upload(self, filepath):
        self.mega.upload(filepath)

        return os.path.basename(filepath)

    @log_download
    def download(self, filename, target_dir=''):
        file = self.mega.find(filename)
        try:
            self.mega.download(file, target_dir)
        except PermissionError as e:
            pass

        return os.path.join(target_dir, filename)

    def serialize(self):
        return {
            "index": self.index,
            "username": self.username,
            "password": self.password
        }


def load_mega_accounts(account_list):
    accounts = []
    for account_json in account_list['mega']:
        accounts.append(MegaStorage(account_json['index'], account_json['id'], account_json['password']))

    return accounts


def get_mega_accounts(account_list):
    mega_accounts = []
    for account in account_list:
        if account.name == "mega":
            mega_accounts.append(account.serialize())
    return mega_accounts

from os import path

from dropbox import dropbox

from core.utils import log_upload, log_download


class DropboxStorage:
    def __init__(self, index, token):
        self.index = index
        self.token = token
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

    def serialize(self):
        return {
            "index": self.index,
            "token": self.token,
        }


def load_dropbox_accounts(account_list):
    accounts = []
    for account_json in account_list['dropbox']:
        accounts.append(DropboxStorage(account_json['index'], account_json['token']))
    return accounts


def get_dropbox_accounts(account_list):
    dropbox_accounts = []
    for account in account_list:
        if account.name == "dropbox":
            dropbox_accounts.append(account.serialize())
    return dropbox_accounts

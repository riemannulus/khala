import hashlib
from os import path
from os import mkdir
from multiprocessing import Process

from core.storage.dropbox import load_dropbox_accounts, get_dropbox_accounts
from core.storage.mega import load_mega_accounts, get_mega_accounts

from core.utils import load_file_list, save_file_list, load_account_list, save_account_list


class Khala:
    # 20971520 == 20MB
    def __init__(self, chunk_size=20971520, temp_path='temp'):
        self.chunk_size = chunk_size
        self.storage_list = load_accounts()
        self.temp_path = temp_path

        if not path.exists(temp_path):
            mkdir(temp_path)

    def chop(self, filename):
        with open(filename, "rb") as f:
            chunk = f.read(self.chunk_size)
            files = []

            while chunk != b"":
                m = hashlib.sha256()
                m.update(chunk)
                chunk_filename = m.hexdigest().__str__()
                with open(path.join(self.temp_path, chunk_filename), "wb") as chunk_f:
                    chunk_f.write(chunk)

                files.append(chunk_filename)
                chunk = f.read(self.chunk_size)
        return files

    def upload(self, filename):
        file_schema = load_file_list()
        files = self.chop(filename)

        storage_count = len(self.storage_list)
        upload_file_chunk_list = []
        procs = []
        for idx, chunk_filename in enumerate(files):
            storage_index = idx % storage_count
            storage = self.storage_list[storage_index]
            proc = Process(
                target=storage.upload,
                args=(path.join(self.temp_path, chunk_filename),))
            procs.append(proc)
            proc.start()
            upload_file_chunk_list.append(
                {
                    "storage": storage.name,
                    "index": storage_index,
                    "chunk_filename": chunk_filename
                }
            )
        file_schema[path.basename(filename)] = upload_file_chunk_list
        save_file_list(file_schema)
        for proc in procs:
            proc.join()

    def download(self, filename, save_name='', save_path=''):
        file_schema = load_file_list()

        chunk_metadata_list = file_schema[filename]

        procs = []
        for idx, metadata in enumerate(chunk_metadata_list):
            storage = self.storage_list[metadata["index"]]
            proc = Process(
                target=storage.download,
                args=(metadata["chunk_filename"], self.temp_path))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        if save_name == '':
            save_name = filename

        with open(path.join(save_path, save_name), "wb") as f:
            for metadata in chunk_metadata_list:
                chunk_name = metadata["chunk_filename"]

                with open(path.join(self.temp_path, chunk_name), "rb") as c:
                    f.write(c.read(self.chunk_size))


def load_accounts():
    account_list = load_account_list()
    accounts = []
    accounts += load_mega_accounts(account_list)
    accounts += load_dropbox_accounts(account_list)

    return sorted(accounts, key=lambda account: account.index)


def append_account(account):
    accounts = load_accounts()
    accounts.append(account)

    save_accounts(sorted(accounts, key=lambda a: a.index))


def save_accounts(account_list):
    latest = account_list[-1].index
    account_json_list = {
        "latest": latest,
        "mega": get_mega_accounts(account_list),
        "dropbox": get_dropbox_accounts(account_list)
    }
    save_account_list(account_json_list)
    return account_json_list

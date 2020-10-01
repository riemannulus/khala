import hashlib
import json
import os
from datetime import datetime

from mega import Mega

target_filename = "target/300M.txt"
distribute_dir = "distributed"
chunk_size = 20 * 1024 * 1024


def load_account_list():
    with open('accounts.json') as json_file:
        return json.load(json_file)


def load_file_list():
    with open('files.json') as json_file:
        return json.load(json_file)


def save_file_list(file_list):
    with open("files.json", "w") as json_file:
        json.dump(file_list, json_file)


def upload(account, filename):
    mega = Mega()
    print(f"[{datetime.now()}] upload start: {filename}")
    mega.login(account["id"], account["password"])
    file = mega.upload(filename)
    print(f"[{datetime.now()}] uploaded: {filename}")
    return mega.get_upload_link(file)


def download(account, filename):
    mega = Mega()
    mega.login(account["id"], account["password"])
    file = mega.find(filename)
    mega.download(file, distribute_dir)


def clear_distribute(file_list):
    for file in file_list:
        os.remove(distribute_dir + "/" + file)


def distributed_upload():
    file_list = load_file_list()

    with open(target_filename, "rb") as f:
        chunk = f.read(chunk_size)
        filelist = []

        while chunk != b"":
            m = hashlib.sha256()
            m.update(chunk)
            chunk_filename = m.hexdigest().__str__()
            with open(distribute_dir + "/" + chunk_filename, "wb") as chunk_f:
                chunk_f.write(chunk)

            filelist.append(chunk_filename)
            chunk = f.read(chunk_size)

    account_list = load_account_list()
    mega_account_list = account_list["mega"]

    account_size = len(mega_account_list)
    upload_file_chunk_list = []
    for idx, chunk_filename in enumerate(filelist):
        account = mega_account_list[idx % account_size]
        upload(account, distribute_dir + "/" + chunk_filename)
        upload_file_chunk_list.append(
            {
                "storage": "mega",
                "index": idx % account_size,
                "chunk_filename": chunk_filename
            }
        )
    file_list[target_filename] = upload_file_chunk_list
    save_file_list(file_list)
    clear_distribute(file_list)


def distributed_download():
    file_list = load_file_list()
    account_list = load_account_list()

    mega_account_list = account_list["mega"]
    chunk_metadata_list = file_list[target_filename]

    for idx, metadata in enumerate(chunk_metadata_list):
        account = mega_account_list[metadata["index"]]
        download(account, metadata["chunk_filename"])

    with open("downloaded_" + target_filename, "wb") as f:
        for metadata in chunk_metadata_list:
            chunk_name = metadata["chunk_filename"]

            with open(distribute_dir + "/" + chunk_name, "rb") as c:
                f.write(c.read(chunk_size))


def standard_upload():
    account_list = load_account_list()

    mega_account_list = account_list["mega"]
    upload(mega_account_list[0], target_filename)


if __name__ == '__main__':
    print(f"[{datetime.now()}] Process start. target file: [{target_filename}]")
    standard_upload()
    print(f"[{datetime.now()}] Process end.")

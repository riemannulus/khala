import hashlib
import json
import os
from datetime import datetime
from multiprocessing import Process

from mega import Mega

filename = "target.dmg"
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
    os.remove(distribute_dir)


def distributed_upload():
    file_list = load_file_list()

    with open(filename, "rb") as f:
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
    procs = []
    for idx, chunk_filename in enumerate(filelist):
        account = mega_account_list[idx % account_size]
        proc = Process(target=upload, args=(account, distribute_dir + "/" + chunk_filename))
        procs.append(proc)
        proc.start()
        upload_file_chunk_list.append(
            {
                "storage": "mega",
                "index": idx % account_size,
                "chunk_filename": chunk_filename
            }
        )
    file_list[filename] = upload_file_chunk_list
    save_file_list(file_list)
    for proc in procs:
        proc.join()


def distributed_download():
    file_list = load_file_list()
    account_list = load_account_list()

    mega_account_list = account_list["mega"]
    chunk_metadata_list = file_list[filename]

    for idx, metadata in enumerate(chunk_metadata_list):
        account = mega_account_list[metadata["index"]]
        download(account, metadata["chunk_filename"])

    with open("downloaded_" + filename, "wb") as f:
        for metadata in chunk_metadata_list:
            chunk_name = metadata["chunk_filename"]

            with open(distribute_dir + "/" + chunk_name, "rb") as c:
                f.write(c.read(chunk_size))


if __name__ == '__main__':
    distributed_upload()

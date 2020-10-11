import functools
import json
from datetime import datetime


def load_account_list():
    with open('accounts.json') as json_file:
        return json.load(json_file)


def load_file_list():
    with open('files.json') as json_file:
        return json.load(json_file)


def save_file_list(file_list):
    with open("files.json", "w") as json_file:
        json.dump(file_list, json_file)


def log_upload(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] upload start: {args[1]}")
        func(*args, **kwargs)
        print(f"[{datetime.now()}] uploaded: {args[1]}")

    return wrapper


def log_download(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] download start: {args[1]}")
        func(*args, **kwargs)
        print(f"[{datetime.now()}] downloaded: {args[1]}")

    return wrapper

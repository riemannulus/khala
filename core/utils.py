import json


def load_account_list():
    with open('accounts.json') as json_file:
        return json.load(json_file)


def load_file_list():
    with open('files.json') as json_file:
        return json.load(json_file)


def save_file_list(file_list):
    with open("files.json", "w") as json_file:
        json.dump(file_list, json_file)

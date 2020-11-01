import argparse
import sys
import time
from datetime import datetime
from pprint import pprint

from gooey import Gooey, GooeyParser

from core.khala import Khala, append_account
from core.storage.dropbox import DropboxStorage
from core.storage.mega import MegaStorage
from core.utils import load_file_list, get_latest_account_index


def upload(filename):
    khala = Khala()
    start_time = datetime.now()
    print(f"[{start_time}] Start upload")
    khala.upload(filename)
    end_time = datetime.now()
    print(f"[{end_time}] Finish upload")
    print(f"Start: {start_time}, End: {end_time}, Record: {end_time-start_time}")


def download(filename):
    khala = Khala()
    start_time = datetime.now()
    print(f"[{start_time}] Start download")
    khala.download(filename)
    end_time = datetime.now()
    print(f"[{end_time}] Finish download")
    print(f"Start: {start_time}, End: {end_time}, Record: {end_time-start_time}")

@Gooey(
    program_name='Test'
)
def main():
    settings_msg = 'Subparser example demonstating bundled configurations ' \
                   'for Siege, Curl, and FFMPEG'
    parser = GooeyParser(description=settings_msg)
    parser.add_argument('--verbose', help='be verbose', dest='verbose',
                        action='store_true', default=False)
    subs = parser.add_subparsers(help='commands', dest='command')

    # ########################################################
    file_parser = subs.add_parser('file', help='curl is a tool to transfer data from or to a server')
    g = file_parser.add_argument_group()
    stuff = g.add_mutually_exclusive_group(
        required=True
    )
    stuff.add_argument(
        '--upload',
        dest='upload',
        widget='FileChooser'
    )
    stuff.add_argument(
        '--download',
        dest='download',
        widget='Dropdown',
        choices=load_file_list()
    )

    # ########################################################
    mega_parser = subs.add_parser(
        'mega', help='Siege is an http/https regression testing and benchmarking utility')
    mega_parser.add_argument('username',
                              help='Pull down headers from the server and display HTTP transaction',
                              type=str)
    mega_parser.add_argument('password',
                              help='Stress the web server with NUM number of simulated users',
                              type=str)

    # ########################################################
    dropbox_parser = subs.add_parser(
        'dropbox', help='Siege is an http/https regression testing and benchmarking utility')
    dropbox_parser.add_argument('token',
                              help='Pull down headers from the server and display HTTP transaction',
                              type=str)

    args = parser.parse_args()
    pprint(args)

    if args.command == "file":
        if args.upload is not None:
            upload(args.upload)
        elif args.download is not None:
            download(args.download)
    if args.command == "mega":
        account_index = get_latest_account_index() + 1
        new_mega = MegaStorage(account_index, args.username, args.password)
        append_account(new_mega)
    if args.command == "dropbox":
        account_index = get_latest_account_index() + 1
        new_dropbox = DropboxStorage(account_index, args.token)
        append_account(new_dropbox)
        pass


if __name__ == '__main__':
    main()

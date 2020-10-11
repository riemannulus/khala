from datetime import datetime

from gooey import Gooey, GooeyParser

from core.khala import Khala
from core.utils import load_file_list


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
    parser = GooeyParser(
        description='example'
    )
    g = parser.add_argument_group()
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

    args = parser.parse_args()

    if args.upload is not None:
        upload(args.upload)
    elif args.download is not None:
        download(args.download)


if __name__ == '__main__':
    main()

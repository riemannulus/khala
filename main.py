from datetime import datetime

from core.khala import Khala


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
    khala.download(filename, save_name="downloaded.exe")
    end_time = datetime.now()
    print(f"[{end_time}] Finish download")
    print(f"Start: {start_time}, End: {end_time}, Record: {end_time-start_time}")


def main(action, filename):
    if action == 'upload':
        upload(filename)
    if action == 'download':
        download(filename)


if __name__ == '__main__':
    main('download', 'target.exe')

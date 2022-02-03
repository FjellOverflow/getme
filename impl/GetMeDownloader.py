import sys

import requests

from util.Logger import GetMeLogger
from abstract.AbstractDownloader import AbstractDownloader
from data.Query import GetMeQueryResult


class GetMeDownloader(AbstractDownloader):

    @staticmethod
    def download_file(download_file: GetMeQueryResult, new_file_name=None) -> str:
        GetMeLogger.log_default(
            f'Downloading file {download_file.get_filename()} from {download_file.get_server_url()} ...\n')
        if not new_file_name:
            new_file_name = download_file.get_filename()

        with open(new_file_name, 'wb') as f:
            response = requests.get(download_file.get_full_path(), stream=True)
            total = response.headers.get('content-length')
            if total is None:
                f.write(response.content)
            else:
                try:
                    downloaded = 0
                    total = int(total)
                    for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                        downloaded += len(data)
                        f.write(data)
                        done = int(50 * downloaded / total)
                        sys.stdout.write('\r{}{}'.format('█' * done, '.' * (50 - done)))
                        sys.stdout.flush()
                except KeyboardInterrupt:
                    GetMeLogger.log_and_abort('Interrupted download.')
        sys.stdout.write('\n')
        GetMeLogger.log_default('\n Finished.')
        return new_file_name

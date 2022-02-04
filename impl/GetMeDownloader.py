import sys

import requests

from data.QueryResult import GetMeQueryResult
from util.Logger import GetMeLogger
from abstract.AbstractDownloader import AbstractDownloader


class GetMeDownloader(AbstractDownloader):
    """A natively implemented downloader"""

    @staticmethod
    def download_file(download_file: GetMeQueryResult, new_file_name=None) -> str:
        """
        Downloads a file for a query result

        :param download_file: the result to download
        :param new_file_name: the name under which the downloaded file is to be saved, optional
        :return: the path of the downloaded file
        """
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
                        sys.stdout.write('\n')
                except KeyboardInterrupt:
                    GetMeLogger.log_and_abort('Interrupted download.')
        GetMeLogger.log_default('\n Finished.')
        return new_file_name

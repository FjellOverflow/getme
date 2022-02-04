import shutil
import subprocess
import sys

from abstract.AbstractDownloader import AbstractDownloader
from data.QueryResult import GetMeQueryResult
from util.Logger import GetMeLogger


class WgetDownloader(AbstractDownloader):
    """A wget-based downloader"""

    @staticmethod
    def download_file(download_file: GetMeQueryResult, new_file_name=None) -> str:
        """
        Downloads a file for a query result

        :param download_file: the result to download
        :param new_file_name: the name under which the downloaded file is to be saved, optional
        :return: the path of the downloaded file
        """

        if shutil.which('wget') is None:
            GetMeLogger.log_important('Can not initialize WgetDownloader. wget is not installed on this machine.')
            sys.exit(1)

        if not new_file_name:
            new_file_name = download_file.get_filename()
        file_url = download_file.get_full_path()
        bash_command = f'wget -O {new_file_name} -c {file_url}'

        GetMeLogger.log_default(f'Built wget-command: {bash_command}')
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        try:
            GetMeLogger.log_default(
                f'Downloading file {download_file.get_filename()} from {download_file.get_server_url()} ...\n')
            process.communicate()
        except KeyboardInterrupt:
            GetMeLogger.log_and_abort('Interrupted download.')

        GetMeLogger.log_default('\n Finished.')
        return new_file_name

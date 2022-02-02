import shutil
import subprocess
import sys

from abstract.AbstractDownloader import AbstractDownloader
from util.Logger import GetMeLogger
from data.Query import GetMeQueryResult


class WgetDownloader(AbstractDownloader):

    @staticmethod
    def download_file(download_file: GetMeQueryResult, new_file_name=None) -> str:
        if shutil.which('wget') is None:
            GetMeLogger.log_important('Can not initialize WgetDownloader. wget is not installed on this machine.')
            sys.exit(1)

        if not new_file_name:
            new_file_name = download_file.get_filename()
        file_url = download_file.get_full_path()
        bash_command = f'wget -O {new_file_name} -c {file_url}'

        GetMeLogger.log_default(f'Built wget-command: {bash_command}')
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        process.communicate()
        return new_file_name

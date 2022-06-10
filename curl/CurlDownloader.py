import shutil
import subprocess
import sys

from abstract.AbstractDownloader import AbstractDownloader
from data.QueryResult import GetMeQueryResult
from impl.GetMeFileNameResolver import GetMeSimpleFileNameResolver
from util.Logger import GetMeLogger


class CurlDownloader(AbstractDownloader):
    """A cUrl based downloader"""

    def __init__(self, file_name_resolver=GetMeSimpleFileNameResolver):
        super().__init__(file_name_resolver)
        self.__file_name_resolver = file_name_resolver()

    def download_file(self, download_file: GetMeQueryResult, new_file_name=None) -> str:
        """
        Downloads a file for a query result

        :param download_file: the result to download
        :param new_file_name: the name under which the downloaded file is to be saved, optional
        :return: the path of the downloaded file
        """

        if shutil.which('curl') is None:
            GetMeLogger.log_important('Can not initialize CurlDownloader. curl is not installed on this machine.')
            sys.exit(1)

        if not new_file_name:
            new_file_name = self.__file_name_resolver.resolve_file_name(download_file.get_filename())

        file_url = download_file.get_full_path()
        bash_command = f'curl -o {new_file_name} {file_url}'

        GetMeLogger.log_default(f'Built curl-command: {bash_command}')
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        try:
            GetMeLogger.log_default(
                f'Downloading file {download_file.get_filename()} from {download_file.get_server_url()} ...\n')
            process.communicate()
        except KeyboardInterrupt:
            GetMeLogger.log_and_abort('Interrupted download.')

        GetMeLogger.log_default('\n Finished.')
        return new_file_name

import abc
from typing import Optional

from data.AggregatedQueryResults import GetMeAggregatedQueryResults
from data.QueryResult import GetMeQueryResult
from util.Logger import GetMeLogger


class AbstractDownloader(abc.ABC):
    """Specifies class signature of a custom downloader"""

    def __init__(self, file_name_resolver: type):
        self.__file_name_resolver = file_name_resolver()

    def offer_downloads(self, query_results: GetMeAggregatedQueryResults) -> Optional[GetMeQueryResult]:
        """
        Present selection of all results for a query and allows selection of one result

        :param query_results: all results to be presented
        :return: the selected result, None if no result was selected
        """
        GetMeLogger.log_verbose('Offering download options:\n')

        entry0 = '(0) Download nothing and exit'
        placeholder = ' ' * len(GetMeLogger.get_log_prefix())
        entries = [f'{placeholder}({index + 1}) {item}' for index, item in enumerate(query_results.get_results())]
        entries.insert(0, entry0)
        GetMeLogger.log_important('\n'.join(entries))

        GetMeLogger.log_important('Your selection: ')
        cmd_line_input = input()
        selected_option = int(cmd_line_input)
        if selected_option == 0:
            GetMeLogger.log_and_exit('Not downloading anything.')
            return
        return query_results.get_results()[selected_option - 1]

    @abc.abstractmethod
    def download_file(self, download_file: GetMeQueryResult, new_file_name=None) -> str:
        """
        Method to be implemented by a custom downloader

        :param download_file: a query result to be downloaded
        :param new_file_name: the name under which the downloaded file is to be saved, optional
        :return: the path of the downloaded file
        """
        pass

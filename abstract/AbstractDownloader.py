import abc
from typing import Optional

from util.Logger import GetMeLogger
from data.Query import GetMeAggregatedQueryResults, GetMeQueryResult


class AbstractDownloader(abc.ABC):

    @staticmethod
    def offer_downloads(query_results: GetMeAggregatedQueryResults) -> Optional[GetMeQueryResult]:
        GetMeLogger.log_verbose('Offering download options:\n')

        entry0 = '(0) Download nothing and exit'
        placeholder = ' '*len(GetMeLogger.get_log_prefix())
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

    @staticmethod
    @abc.abstractmethod
    def download_file(download_file: GetMeQueryResult, new_file_name=None) -> str:
        pass

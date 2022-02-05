import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from bs4 import BeautifulSoup

from data.AggregatedQueryResults import GetMeAggregatedQueryResults
from data.QueryResult import GetMeQueryResult
from util.Logger import GetMeLogger
from abstract.AbstractSourceAdapter import AbstractSourceAdapter
from data.Query import GetMeQuery, GetMeQueryType

FILEPURSUIT_QUERY_TYPES = ['all', 'video', 'audio', 'ebook', 'mobile', 'archive']


class FilePursuitAdapter(AbstractSourceAdapter):
    """Implements a source adapter for FilePursuit"""

    @staticmethod
    def _translate_to_filepursuit_query_types(getme_query_types: [GetMeQueryType]) -> [str]:
        """
        Matches native query-types with FilePursuit query types

        :param getme_query_types: native query types
        :return: matching FilePursuit query types
        """
        filepursuit_query_types = []
        for getme_query_type in getme_query_types:
            if getme_query_type.value in FILEPURSUIT_QUERY_TYPES:
                filepursuit_query_types.append(getme_query_type.value)

        if not filepursuit_query_types:
            filepursuit_query_types = ['all']

        GetMeLogger.log_verbose(
            f'Translated requested query-types to FilePursuit query-types [{", ".join(filepursuit_query_types)}].')
        return filepursuit_query_types

    @staticmethod
    def _translate_to_getme_query_type(filepursuit_query_type: str) -> Optional[GetMeQueryType]:
        """
        Matches a FilePursiut query type with a native query type

        :param filepursuit_query_type: FilePursuit query type
        :return: a native query type if matched, else None
        """
        try:
            return GetMeQueryType(filepursuit_query_type)
        except ValueError:
            return None

    def get_query_results(self, query: GetMeQuery) -> GetMeAggregatedQueryResults:
        """
        Fetches results for query from FilePursuit

        :param query: the query to search for
        :return: the FilePursuit results
        """
        results = []
        max_results = query.get_max_number_results()
        if not max_results:
            max_results = 50

        filepursuit_query_types = self._translate_to_filepursuit_query_types(query.get_query_types())
        for query_type in filepursuit_query_types:
            start_row = 0
            file_urls = []
            while len(results) < max_results and (start_row == 0 or len(file_urls) == 50):
                filepursuit_query = self._build_file_pursuit_query(query, query_type, start_row)
                webpage = self._download_filepursuit_query_result(filepursuit_query)
                file_urls = self._parse_filepursuit_query_results(webpage)
                results.extend(
                    [GetMeQueryResult(u, self._translate_to_getme_query_type(query_type)) for u in file_urls])
                start_row += 50

        GetMeLogger.log_default(f'Extracted {len(results)} results for query.')
        return GetMeAggregatedQueryResults(query, results)

    @staticmethod
    def _build_file_pursuit_query(query: GetMeQuery, filepursuit_query_type, start_row: int) -> str:
        """
        Builds url to query FilePursuit

        :param query: the query
        :param filepursuit_query_type: the matched FilePursuit query types
        :return: the built url
        """
        base_url = 'https://filepursuit.com/pursuit?'
        param_sep = '&'
        string_sep = '+'
        param_query = 'q'
        param_type = 'type'
        param_start_row = 'startrow'
        query_no_whitespaces = query.get_query().replace(' ', string_sep)
        filepursuit_url = f'{base_url}{param_query}={query_no_whitespaces}{param_sep}{param_type}=' \
                          f'{filepursuit_query_type}{param_sep}{param_start_row}={start_row}'
        GetMeLogger.log_default(f'Built FilePursuit query-url: \"{filepursuit_url}\".')
        return filepursuit_url

    @staticmethod
    def _download_filepursuit_query_result(filepursuit_query_url: str) -> str:
        """
        Downloads the html of queried FilePursuit site

        :param filepursuit_query_url: the FilePursuit url
        :return: the html-content
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                          'Chrome/23.0.1271.64 Safari/537.11'
        }
        request = urllib.request.Request(filepursuit_query_url, headers=headers)
        response = urllib.request.urlopen(request)
        webpage = response.read().decode('UTF-8')
        GetMeLogger.log_verbose('Downloaded FilePursuit query-results webpage.')
        return webpage

    @staticmethod
    def _parse_filepursuit_query_results(webpage: str) -> [str]:
        """
        Search FilePursuit html for potential results

        :param webpage: FilePursuit html content
        :return: list of extracted urls
        """
        GetMeLogger.log_verbose('Extracting urls from webpage.')
        file_urls = []

        soup = BeautifulSoup(webpage, 'html.parser')
        all_entries = soup.find_all('div', class_='file-post-item')

        GetMeLogger.log_verbose(f'Found {len(all_entries)} items.')
        for entry in all_entries:
            start_index = str(entry).lower().find('copytoclipboard')
            end_index = str(entry).lower().find('\')" style')
            file_url = str(entry)[start_index + 17:end_index]
            file_urls.append(file_url.replace(' ', '%20'))

        return file_urls

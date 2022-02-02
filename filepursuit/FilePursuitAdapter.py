import urllib.error
import urllib.parse
import urllib.request
from typing import Optional

from bs4 import BeautifulSoup

from util.Logger import GetMeLogger
from abstract.AbstractSourceAdapter import AbstractSourceAdapter
from data.Query import GetMeQuery, GetMeAggregatedQueryResults, GetMeQueryResult, GetMeQueryType

FILEPURSUIT_QUERY_TYPES = ['all', 'video', 'audio', 'ebook', 'mobile', 'archive']


class FilePursuitAdapter(AbstractSourceAdapter):

    @staticmethod
    def _translate_to_filepursuit_query_types(getme_query_types: [GetMeQueryType]) -> [str]:
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
        try:
            return GetMeQueryType(filepursuit_query_type)
        except ValueError:
            return None

    def get_query_results(self, query: GetMeQuery) -> GetMeAggregatedQueryResults:
        results = []

        filepursuit_query_types = self._translate_to_filepursuit_query_types(query.get_query_types())
        for query_type in filepursuit_query_types:
            filepursuit_query = self._build_file_pursuit_query(query, query_type)
            webpage = self._download_filepursuit_query_result(filepursuit_query)
            file_urls = self._parse_filepursuit_query_results(webpage)
            results.extend([GetMeQueryResult(u, self._translate_to_getme_query_type(query_type)) for u in file_urls])

        GetMeLogger.log_default(f'Extracted {len(results)} for query.')
        return GetMeAggregatedQueryResults(query, results)

    @staticmethod
    def _build_file_pursuit_query(query: GetMeQuery, filepursuit_query_type) -> str:
        base_url = 'https://filepursuit.com/pursuit?'
        param_sep = '&'
        string_sep = '+'
        param_query = 'q'
        param_type = 'type'
        query_no_whitespaces = query.get_query().replace(' ', string_sep)
        filepursuit_url = f'{base_url}{param_query}={query_no_whitespaces}{param_sep}{param_type}=' \
                          f'{filepursuit_query_type} '
        GetMeLogger.log_default(f'Built FilePursuit query-url: \"{filepursuit_url}\".')
        return filepursuit_url

    @staticmethod
    def _download_filepursuit_query_result(filepursuit_query_url: str) -> str:
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

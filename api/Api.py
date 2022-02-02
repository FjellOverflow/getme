from typing import Optional

from data.Query import GetMeQueryType, GetMeQuerySource, GetMeQuery, GetMeAggregatedQueryResults
from filepursuit.FilePursuitAdapter import FilePursuitAdapter
from util.Logger import GetMeLoggerMode, GetMeLogger


class GetMeApi:

    def __init__(self, logger_mode=GetMeLoggerMode.DEFAULT):

        GetMeLogger(logger_mode)
        GetMeLogger.log_verbose(f'Set up logger with mode {logger_mode.name}.')

    @staticmethod
    def _extract_getme_query_types(query_types: [str]) -> [GetMeQueryType]:
        getme_query_types = []
        for query_type in query_types:
            try:
                getme_query_types.append(GetMeQueryType(query_type))
            except ValueError:
                continue
        return getme_query_types

    @staticmethod
    def _extract_getme_source(source: str) -> Optional[GetMeQuerySource]:
        try:
            return GetMeQuerySource(source)
        except ValueError:
            return

    @staticmethod
    def build_query(query: str, query_types: [GetMeQueryType], query_source: GetMeQuerySource):

        if not query or not query_types or not query_source:
            GetMeLogger.log_and_abort('Query options were malformed.')

        GetMeLogger.log_default(
            f'Received query \"{query}\" of type(s) [{", ".join([t.name for t in query_types])}] '
            f'for source {query_source.name}.')

        query_object = GetMeQuery(query, query_types, query_source)
        return query_object

    @staticmethod
    def execute_query(query: GetMeQuery) -> [GetMeAggregatedQueryResults]:

        adapter_matching = {
            GetMeQuerySource.GOOGLE: None,
            GetMeQuerySource.FILEPURSUIT: FilePursuitAdapter
        }
        adapter = adapter_matching[query.get_query_source()]
        if adapter:
            GetMeLogger.log_verbose(f'Matched adapter for source {query.get_query_source().name}.')
        else:
            GetMeLogger.log_default(f'Adapter for source {query.get_query_source().name} not implemented yet.')

        results = adapter().get_query_results(query)
        return results

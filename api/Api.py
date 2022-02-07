from data.AggregatedQueryResults import GetMeAggregatedQueryResults
from data.Query import GetMeQueryType, GetMeQuerySource, GetMeQuery
from filepursuit.FilePursuitAdapter import FilePursuitAdapter
from util.Logger import GetMeLoggerMode, GetMeLogger


class GetMeApi:
    """Api to use GetMe"""

    def __init__(self, logger_mode=GetMeLoggerMode.DEFAULT):
        """Sets up GetMe-API with logger"""

        GetMeLogger(logger_mode)
        GetMeLogger.log_verbose(f'Set up logger with mode {logger_mode.name}.')

    @staticmethod
    def build_query(query: str, query_types: [GetMeQueryType], query_source: GetMeQuerySource,
                    max_results=50) -> GetMeQuery:
        """
        Builds GetMeQuery from query, types and source

        :param query: the string to search for
        :param query_types: list of media-types to search for
        :param query_source: source to search
        :param max_results: max number of results to search for
        :return:
        """

        if not query or not query_types or not query_source:
            GetMeLogger.log_and_abort('Query options were malformed.')

        GetMeLogger.log_default(
            f'Received query \"{query}\" of type(s) [{", ".join([t.name for t in query_types])}] '
            f'for source {query_source.name}.')

        query_object = GetMeQuery(query, query_types, query_source, max_results)
        return query_object

    @staticmethod
    def execute_query(query: GetMeQuery) -> [GetMeAggregatedQueryResults]:
        """
        Executes a query by the matching adapter for source

        :param query: query to execute
        :return: the results of the executed query
        """

        adapter_matching = {
            GetMeQuerySource.GOOGLE: None,
            GetMeQuerySource.FILEPURSUIT: FilePursuitAdapter
        }
        adapter = adapter_matching[query.get_query_source()]
        if adapter:
            GetMeLogger.log_verbose(f'Matched adapter for source {query.get_query_source().name}.')
        else:
            GetMeLogger.log_and_abort(f'Adapter for source {query.get_query_source().name} not implemented yet.')

        results = adapter().get_query_results(query)
        return results

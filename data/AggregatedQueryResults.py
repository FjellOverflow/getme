from data.Query import GetMeQuery
from data.QueryResult import GetMeQueryResult


class GetMeAggregatedQueryResults:
    """Holds data for a collection of results for query"""

    def __init__(self, query: GetMeQuery, results: [GetMeQueryResult]):
        self.__query = query
        self.__results = results

    def get_query(self) -> GetMeQuery:
        return self.__query

    def get_results(self) -> [GetMeQueryResult]:
        return self.__results

    def get_results_by_server(self, server: str) -> [GetMeQueryResult]:
        return [r for r in self.__results if r.get_server_url() == server]

    def get_results_by_file_extension(self, file_extension: str) -> [GetMeQueryResult]:
        file_extension.replace('.', '')
        file_extension = file_extension.lower()
        return [r for r in self.__results if r.get_file_extension() == file_extension]

    def __repr__(self):
        return '\n'.join([str(r) for r in self.__results])

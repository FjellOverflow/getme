import enum


class GetMeQuerySource(enum.Enum):
    FILEPURSUIT = 'filepursuit'
    GOOGLE = 'google'


class GetMeQueryType(enum.Enum):
    VIDEO = 'video'
    AUDIO = 'audio'
    EBOOK = 'ebook'


class GetMeQuery:
    """Holds data for a query"""

    def __init__(self, query: str, query_types: [GetMeQueryType], query_source: GetMeQuerySource,
                 max_number_results: int):
        self.__query = query
        self.__query_types = query_types
        self.__query_source = query_source
        self.__max_number_results = max_number_results

    def get_max_number_results(self) -> int:
        return self.__max_number_results

    def get_query(self) -> str:
        return self.__query

    def get_query_types(self) -> [GetMeQueryType]:
        if self.__query_types:
            return self.__query_types
        return [t for t in GetMeQueryType]

    def get_query_source(self) -> [GetMeQuerySource]:
        if self.__query_source:
            return self.__query_source
        return [s for s in GetMeQuerySource][0]

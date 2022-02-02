import enum


class GetMeQuerySource(enum.Enum):
    FILEPURSUIT = 'filepursuit'
    GOOGLE = 'google'


class GetMeQueryType(enum.Enum):
    VIDEO = 'video'
    AUDIO = 'audio'
    EBOOK = 'ebook'


class GetMeQuery:

    def __init__(self, query: str, query_types: [GetMeQueryType], query_source: GetMeQuerySource):
        self.__query = query
        self.__query_types = query_types
        self.__query_source = query_source

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


class GetMeQueryResult:

    def __init__(self, file_url: str, query_type: GetMeQueryType):
        self.__file_url = file_url
        self.__query_type = query_type

    def get_server_url(self):
        first_occ = self.__file_url.find('/')
        second_occ = self.__file_url.find('/', first_occ + 1)
        end_index = self.__file_url.find('/', second_occ + 1)
        return self.__file_url[0:end_index].lower()

    def get_filename(self):
        start_index, new_index = 0, 0
        while new_index != -1:
            start_index = new_index
            new_index = self.__file_url.find('/', start_index + 1)
        return self.__file_url[start_index + 1:]

    def get_file_extension(self):
        start_index, new_index = 0, 0
        while new_index != -1:
            start_index = new_index
            new_index = self.__file_url.find('.', start_index + 1)
        return self.__file_url[start_index + 1:].lower()

    def get_full_path(self):
        return self.__file_url

    def __repr__(self):
        return self.__file_url


class GetMeAggregatedQueryResults:

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

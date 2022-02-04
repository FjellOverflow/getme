from data.Query import GetMeQueryType


class GetMeQueryResult:
    """Holds data for a result of a query"""

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

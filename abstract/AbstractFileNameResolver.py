import abc


class AbstractFileNameResolver(abc.ABC):
    """Specifies class signature of a custom file name resolver"""

    @abc.abstractmethod
    def resolve_file_name(self, original_file_name: str) -> str:
        """
        Method to be implemented by custom file name resolver

        :param original_file_name: complete url of the file to parse name from
        :return: the suggested file name
        """
        pass

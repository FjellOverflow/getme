import abc

from data.AggregatedQueryResults import GetMeAggregatedQueryResults
from data.Query import GetMeQuery


class AbstractSourceAdapter(abc.ABC):
    """Specifies the class signature of a custom source adapter"""

    @abc.abstractmethod
    def get_query_results(self, query: GetMeQuery) -> GetMeAggregatedQueryResults:
        """
        Method to be implemented by a custom source adapter

        :param query: query to be executed
        :return: results of the given query
        """
        pass

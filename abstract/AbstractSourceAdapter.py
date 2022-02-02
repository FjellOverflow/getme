import abc

from data.Query import GetMeQuery, GetMeAggregatedQueryResults


class AbstractSourceAdapter(abc.ABC):

    @abc.abstractmethod
    def get_query_results(self, query: GetMeQuery) -> GetMeAggregatedQueryResults:
        pass

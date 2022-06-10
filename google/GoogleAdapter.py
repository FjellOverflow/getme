from abstract.AbstractSourceAdapter import AbstractSourceAdapter
from data.AggregatedQueryResults import GetMeAggregatedQueryResults
from data.Query import GetMeQuery, GetMeQueryType


# TODO
class GoogleAdapter(AbstractSourceAdapter):
    """Implements a source adapter for Google"""

    @staticmethod
    def build_google_query(searchphrase: str, query_type: GetMeQueryType) -> str:
        """
        Builds query url for Google

        :param searchphrase: the filename to search for
        :param query_type: the type of media to search for
        :return: the built google url
        """
        google_query_matching = {
            GetMeQueryType.VIDEO: '(.mkv|.mp4|.avi|.mov|.mpg|.wmv)',
            GetMeQueryType.AUDIO: '(.ogg|.mp3|.flac|.wma|.m4a)',
            GetMeQueryType.EBOOK: '(.MOBI|.CBZ|.CBR|.CBC|.CHM|.EPUB|.FB2|.LIT|.LRF|.ODT|.PDF|.PRC|.PDB|.PML|.RB|.RTF'
                                  '|.TCR) '
        }

        google_query_type = google_query_matching[query_type]
        url = f'https://www.google.com/search?q=%2B{google_query_type}%20+{searchphrase}%20+intitle:%22index' \
              f'%20of%22%20-inurl:(jsp|pl|php|html|aspx|htm|cf|shtml)%20-inurl:(' \
              f'hypem|unknownsecret|sirens|writeups|trimediacentral|articlescentral|listen77|mp3raid|mp3toss' \
              f'|mp3drug|theindexof|index_of|wallywashis|indexofmp3) '
        return url

    def get_query_results(self, query: GetMeQuery) -> GetMeAggregatedQueryResults:
        """
        Fetches results for query from Google

        :param query: the query to search for
        :return: the Google results
        """
        for native_type in query.get_query_types():
            url = self.build_google_query(query.get_query(), native_type)
            print(url)

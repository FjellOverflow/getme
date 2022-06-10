import datetime

from abstract.AbstractFileNameResolver import AbstractFileNameResolver


class GetMeSimpleFileNameResolver(AbstractFileNameResolver):
    """A natively implemented simple file name resolver"""

    def resolve_file_name(self, original_file_name: str) -> str:
        """
        Parse a suggested file name from a file url

        :param original_file_name: complete url of the file to parse name from
        :return: the suggested file name
        """
        return original_file_name


class GetMeAdvancedFileNameResolver(AbstractFileNameResolver):
    """A natively implemented file name resolver"""

    def resolve_file_name(self, original_file_name: str) -> str:
        """
        Parse a suggested file name from a file url

        :param original_file_name: complete url of the file to parse name from
        :return: the suggested file name
        """

        new_file_name = original_file_name
        list_eliminate_strs = [
            'BrRip',
            '480p',
            '720p',
            '1080p',
            'HD',
            'WEB-DL',
            'BDRip',
            'DVDRip',
            'x264',
            'H264'
            'XviD',
            'BluRay',
            'Subbed',
            'Dubbed',
            'AAC-RARBG',
            'CAM',
            'Rip',
            'YIFY',
            '(',
            ')'
        ]
        list_whitespace_strs = [
            '%20',
            '-',
            '_'
        ]
        for el_str in list_eliminate_strs:
            new_file_name = new_file_name.replace(el_str, '')

        for el_str in list_whitespace_strs:
            new_file_name = new_file_name.replace(el_str, ' ')

        start_year = 1900
        end_year = int(datetime.datetime.now().date().strftime("%Y"))
        while start_year <= end_year:
            new_file_name = new_file_name.replace(str(start_year), '')
            start_year += 1

        return new_file_name

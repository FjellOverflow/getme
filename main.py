#!/usr/bin/env python3
import getopt
import sys

from api.Api import GetMeApi
from data.Query import GetMeQuerySource, GetMeQueryType
from impl.GetMeDownloader import GetMeDownloader
from util.Logger import GetMeLoggerMode
from wget.WgetDownloader import WgetDownloader

GETME_INFO_MESSAGE = f'Usage: getme --query <query> [--source <source>] [-v, -a, -e, -q, -a]\n\n' \
                     '  QUERY \n' \
                     f'      <query>             The file to search for \n' \
                     f'      <source> (Optional) One of the following: ' \
                     f'{", ".join([s.value for s in GetMeQuerySource])} ' \
                     f'\n\n' \
                     '  OPTIONS \n' \
                     '      -v       (Optional) video - search for video \n' \
                     '      -a       (Optional) audio - Search for audio \n' \
                     '      -e       (Optional) e-books - search for e-books \n\n' \
                     '  LOGGING \n' \
                     '      -q       (Optional) quiet - no non-essential logging \n' \
                     '      -f       (Optional) full - all logging enabled \n\n' \
                     '  OTHER \n' \
                     '      -h       (Optional) help - pring this message'

if __name__ == '__main__':
    query = None
    query_types = []
    query_source = None
    logger_mode = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vaeqfh', ['query=', 'source='])
    except getopt.GetoptError:
        print(GETME_INFO_MESSAGE)
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-v':
            query_types.append(GetMeQueryType.VIDEO)
        elif opt == '-a':
            query_types.append(GetMeQueryType.AUDIO)
        elif opt == '-e':
            query_types.append(GetMeQueryType.EBOOK)
        elif opt == '-q':
            logger_mode = GetMeLoggerMode.QUIET
        elif opt == '-f':
            logger_mode = GetMeLoggerMode.VERBOSE
        elif opt == '-h':
            print(GETME_INFO_MESSAGE, True)
            sys.exit()
        elif opt == '--query':
            query = arg
        elif opt == '--source':
            try:
                query_source = GetMeQuerySource(arg)
            except ValueError:
                print(f'[getme]: Source {arg} not recognized.')

    if not query_source:
        query_source = GetMeQuerySource.GOOGLE

    if not query_types:
        query_types = [t for t in GetMeQueryType]

    if not logger_mode:
        logger_mode = GetMeLoggerMode.DEFAULT

    api = GetMeApi(logger_mode)

    getme_query = api.build_query(query, query_types, query_source)
    results = api.execute_query(getme_query)

    downloader = WgetDownloader()
    chosen_file = downloader.offer_downloads(results)
    if chosen_file:
        downloader.download_file(chosen_file)

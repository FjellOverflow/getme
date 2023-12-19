
<h1 align="center">
  GetMe
  <br>
</h1>

<h4 align="center">An open-directory command-line utility built with Python</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How to use</a> •
  <a href="#extensions">Extensions</a> •
  <a href="#coming-features">Coming features</a>
</p>

## Key Features

* Search for specific files in open directories
  - Supports different sources like [FilePursuit](https://filepursuit.com/), [Google](https://www.google.com/), ...
* Search for specific file-types like videos, music, ...
* Filter results by server, file-extensions, ...
* Download found files instantly
* Extend with custom components for external services


## How to use
### Command line
```bash
# main.py calls the command-line wrapper
# flag -h shows help
>> ./main.py -h
Usage: getme --query <query> [--source <source>] [-v, -a, -e, -q, -a]

  QUERY
      <query>             The file to search for
      <source> (Optional) One of the following: filepursuit, google

  OPTIONS
      -v       (Optional) video - search for video
      -a       (Optional) audio - Search for audio
      -e       (Optional) e-books - search for e-books

  LOGGING
      -q       (Optional) quiet - no non-essential logging
      -f       (Optional) full - all logging enabled

  OTHER
      -h       (Optional) help - print this message
      
# search FilePursuit for video-files named "Never gonna give you up"
>> ./main.py -v --source filepursuit --query "Never gonna give you up"
[getme]: Received query "Never gonna give you up" of type(s) [VIDEO] for source FILEPURSUIT.
[getme]: Built FilePursuit query-url: "https://filepursuit.com/pursuit?q=Never+gonna+give+you+up&type=video ".
[getme]: Extracted 3 results for query.
[getme]: (0) Download nothing and exit
         (1) http://first-server/never/gonna/give/you/up/video.mp4
         (2) http://secondserver/music/rickastley/nevergonnagiveyouup.mkv
         (3) http://third.server/abc/def/never-gonna-give-you-up.flv
[getme]: Your selection: 2
[getme]: Downloading file nevergonnagiveyouup.mkv ...
[getme]: Finished.
```

### Python
```py
from api.Api import GetMeApi
from data.Query import GetMeQuerySource, GetMeQueryType
from impl.GetMeDownloader import GetMeDownloader

# we initiate the GetMe-API
api = GetMeApi()

# we build the query
searchphrase = "Never gonna give you up"
types = [GetMeQueryType.VIDEO]
source = GetMeQuerySource.FILEPURSUIT
query = api.build_query(searchphrase, types, source)

# we get results from query execution
results = api.execute_query(query)

# we initiate a downloader
downloader = GetMeDownloader()

# we download the 2nd result
downloader.download_file(results[1])
```

## Extensions
As GetMe is structured into seperate components, it can be extended with custom components, namely SearchAdapters and Downloaders.

### Custom downloader
A downloader extends the functionality of the `AbstractDownloader`
```py
from data.QueryResult import GetMeQueryResult
from abstract.AbstractDownloader import AbstractDownloader

class MyCustomDownloader(AbstractDownloader):

    @staticmethod
    def download_file(download_file: GetMeQueryResult, new_file_name=None) -> str:
        # function takes as input file to download and potentially a filename
        # name the downloaded file according to "new_file_name" if it was provided
        # return path to downloaded file

        # do some stuff

        return new_file_name
```

### Custom SourceAdapter
A SourceAdapter extends the functionality of the `AbstractSourceAdapter`
```py
from data.AggregatedQueryResults import GetMeAggregatedQueryResults
from abstract.AbstractSourceAdapter import AbstractSourceAdapter
from data.Query import GetMeQuery

class MyCustomSourceAdapter(AbstractSourceAdapter):

    def get_query_results(self, query: GetMeQuery) -> GetMeAggregatedQueryResults:
        results = []

        # fetch the results however you like
        # return an instance of GetMeAggregatedQueryResults
        # containing the query and your results

        # do some stuff

        return GetMeAggregatedQueryResults(query, results)

```

## Coming features

| Feature | Description | Internal component | External component | In progress |
|- | - | - | - | - |
| Implement Google source adapter | Search Google for files | New source adapter  | [Google](https://www.google.com/) | Yes |
| Multisource adapter | Search multiple sources at once | New native component |
| Filename parser | Extract proper filename from url | New native component |
| Server ratings | Rank/ blacklist/ avoid known servers when searching | Source adapters |
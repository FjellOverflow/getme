from api.Api import GetMeApi
from data.Query import GetMeQueryType, GetMeQuerySource
from util.Logger import GetMeLoggerMode

# setting up API with verbose logging
api = GetMeApi(GetMeLoggerMode.VERBOSE)

# building a query
searchphrase = "Never gonna give you up"
types = [GetMeQueryType.VIDEO]
source = GetMeQuerySource.FILEPURSUIT
max_number_of_results = 100
query = api.build_query(searchphrase, types, source, max_number_of_results)

# executing query
results = api.execute_query(query)

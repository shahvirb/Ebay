import sys
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from accounts import PRODUCTION_APPID
from ebay_processing import response_to_dataframe
import os
import search_queries

# Use a variable to refer to the query and the output files to make it easier to manage multiple queries.
query_arg = sys.argv[1]
# Converts the query argument into a variable called query
exec('query = search_queries.' + query_arg)

try:
    api = Finding(appid=PRODUCTION_APPID, config_file=None)
    response = api.execute('findCompletedItems', query)
    df = response_to_dataframe(response)
    print(df.head())
    df.to_excel(
        'Results_' + query_arg + '.xlsx',
        sheet_name='Results',
        index=False
    )
except ConnectionError as e:
    print(e)
    print(e.response.dict())


def find_sensitive_path(directory, insensitive_path):
    """
    Perform a case insensitive search for the query file name.
    """
    insensitive_path = insensitive_path.strip(os.path.sep)

    parts = insensitive_path.split(os.path.sep)
    next_name = parts[0]
    for name in os.listdir(directory):
        if next_name.lower() == name.lower():
            improved_path = os.path.join(directory, name)
            if len(parts) == 1:
                return improved_path
            else:
                return find_sensitive_path(improved_path, os.path.sep.join(parts[1:]))
    return None

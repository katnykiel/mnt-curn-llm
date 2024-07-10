from dotenv import load_dotenv
from newsapi import NewsApiClient
import json
import os

load_dotenv()
api_key = os.getenv('api_key')

# Query news api for heaflines about climate change
newsapi = NewsApiClient(api_key)
get_everything = newsapi.get_everything(q='climate change',
                                        language='en',
                                        sort_by='relevancy',
                                        page = 1)

# Store the data in a json file
#with open("data.json", "w") as f:
#    json.dump(get_everything,f)

print(get_everything)
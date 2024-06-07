from newsapi import NewsApiClient
import json

# Query news api for heaflines about climate change
newsapi = NewsApiClient(api_key='API_KEY')
get_everything = newsapi.get_everything(q='climate change',
                                        language='en',
                                        sort_by='relevancy',
                                        page = 1)

# Store the data in a json file
with open("data.json", "w") as f:
    json.dump(get_everything,f)

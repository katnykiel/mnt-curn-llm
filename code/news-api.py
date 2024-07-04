from newsapi import NewsApiClient
import json

# Query news api for heaflines about climate change
newsapi = NewsApiClient(api_key='b44ee29880524e4a80ed16da906fb0f8')
get_everything = newsapi.get_everything(q='climate change',
                                        language='en',
                                        sort_by='relevancy',
                                        page = 1)

# Store the data in a json file
with open("data.json", "w") as f:
    json.dump(get_everything,f)

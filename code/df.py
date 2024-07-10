import json
import pandas as pd

'''with open('data.json', 'r') as f:
    data = json.load(f)
urls = []
#print(data)
for articles in data["articles"]:
    if "url" in articles:
        urls.append(articles["url"])
print(urls)'''

#load dataframe
df = pd.read_excel("/Users/bryan/Work/MNT-CURN/Purdue Internship/mnt-curn-llm/Book1.xlsx")
#extracts all urls from column and turns it into a list
urls = list(df['URLS'].unique())
experts = list(df['Experts'].unique())
#clears the NaN from the list
urls = [url for url in urls if pd.notna(url)]
#print(experts)

grouped = df.groupby("URLS")["Experts"].apply(list).reset_index()
list_of_lists = grouped['Experts'].tolist()

print(list_of_lists)
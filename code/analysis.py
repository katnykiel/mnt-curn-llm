import pandas as pd
import json
import math
import numpy as np
import pandas as pd 
import plotly.graph_objects as go

from collections import Counter
from textblob import TextBlob

df = pd.read_excel('data/Book1.xlsx',index_col=0) # Reads CSV file
print(df.head())


experts = df['Experts'].values
unique_experts = list(set(experts))
experts_counts = np.zeros(len(unique_experts))
print(unique_experts)
for i, unique in enumerate(unique_experts):
   count = 0
   for j in range(len(experts)):
       if (experts[j] == unique):
           count += 1
   experts_counts[i] = count

# Display histogram of entity data
fig = go.Figure()
fig.add_trace(go.Histogram(x=experts_counts, hovertext = unique_experts))
fig.update_layout(xaxis_title='Experts',template='simple_white', yaxis_title='Count', width=600,height=400, title='Manually Labeled Experts')
fig.show()

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import datetime
timestamp = str(datetime.datetime.now())


data = pd.read_html('http://codemasters.eng.unimelb.edu.au/lb.html')
df_pl = data[0]
# getting rid of the lines
df_pl.dropna(inplace=True)

new_header = df_pl.iloc[0] #grab the first row for the header
df = df_pl[1:] #take the data less the header row
df.columns = new_header

df.to_csv('Leaderboard'+timestamp+'.csv', encoding='utf-8', index=False)
import pandas as pd

df = pd.read_csv("data/continent_country.csv")

df.drop(columns=['Continent_Code','Two_Letter_Country_Code','Country_Number','Country_Name'] ,axis=0)

g = df.groupby(['Continent_Name'])

for data_df in g:
    print(data_df[0])

for data_d in g:
    print(data_d[0], data_d[1]['Three_Letter_Country_Code'].values)

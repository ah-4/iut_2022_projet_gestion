import pandas as pd
import sqlite3 as sql

df = pd.read_csv('laptndesaecmort\sus.csv')
con = sql.connect('example.sqlite')
cur = con.cursor()
#cur.execute("drop table pays")
cur.execute("create table pays (CountryCode, IncomeGroup)")
# This is the qmark style:
cur.execute("insert into pays values (?, ?)", ('FRA', "High Income"))

# The qmark style used with executemany():
country_list = []
for i in range(len(df.values)):
    z = (df.get('Country Code').values[i],df.get('IncomeGroup').values[i])
    country_list.append(z)


print(country_list)
cur.executemany("insert into pays values (?, ?)", country_list)

# And this is the named style:
cur.execute("select * from pays")
print(cur.fetchall())

con.close()
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import base64
import sqlite3 as sql

app = dash.Dash(__name__)

con = sql.connect('laptndesaecmort\GeoDatabase.db', check_same_thread=False)
cur = con.cursor()
cur.execute("SELECT NomPays FROM Pays")
#print(cur.fetchall())
pays = cur.fetchall()
print(pays[0][0])
pays = [sublist[0] for sublist in pays]
print(pays)
'''
cur.execute("drop table pays")
cur.execute("create table pays (CountryCode, IncomeGroup)")

# The qmark style used with executemany():
country_list = []
for i in range(len(df.values)):
    z = (df.get('Country Code').values[i],df.get('IncomeGroup').values[i])
    country_list.append(z)

cur.executemany("insert into pays values (?, ?)", country_list)
'''

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

image_filename = 'laptndesaecmort/babyfoot.png'
cur.execute("SELECT CodePays from pays")
print(pays[0])
app.layout = html.Div(
    children=[
        html.H1(children="CaféPierre Analytics"),
        html.P(
            children="Cet outil a pour but de vous aider à analyser les différentes données autour de la polution à travers le monde",
        ),
        html.Img(src=b64_image(image_filename)),

        dcc.Dropdown(
            id="dropDownPays",
            value = str(pays[0]),
            options=[
                {"label": area, "value": area} for area in pays
            ],
            
        ),
        html.Br(),
        html.Div(id="report"),
    ]
)

# 4. Callback
@app.callback(Output("report", "children"), Input("country", "value"))
def display_country_report(country):
    cur.execute("SELECT NomPays FROM pays WHERE CodePays = " + country)
    return cur.fetchone()

if __name__ == "__main__":
    app.run_server()

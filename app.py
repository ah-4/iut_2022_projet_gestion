from distutils.log import debug
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import base64
import matplotlib.pyplot as plt
import sqlite3 as sql
import geopandas as gpd
import netCDF4 as nc
import xarray as xr

feuillesExternes = [
    {
        "href": "assets/feuilleDeStyle.css",
        "rel":"stylesheet",
    },
]
app = dash.Dash(__name__,external_stylesheets=feuillesExternes,update_title="Chargement...")
app.title = "Outils de visualisation de données pour CafePierre"

con = sql.connect('GeoDatabase.db', check_same_thread=False)
cur = con.cursor()
'''
cur.execute("SELECT * FROM Informer INNER JOIN TypeDeDonnee ON ")
print(cur.fetchall())
pays = cur.fetchall()
pays = [sublist[0] for sublist in pays]'''
pays = []
event = None

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

cur.execute("SELECT CodePays from pays")
app.layout = html.Div(
    children=[
        html.H1(children="CaféPierre Analytics"),
        html.P(
            children="Cet outil a pour but de vous aider à analyser les différentes données autour de la polution à travers le monde",
        ),

        dcc.Dropdown(
            id="dropDownPays",
            placeholder="Sélectionnez le pays ou la zone géographique recherchée :",
            multi=True,
            options=[
                {"label": area, "value": area} for area in pays
            ],
            
        
        ),
        html.Br(),

        html.Div(id="report"),

        html.Img(src=b64_image("levelMap.png"),className="carte")
    ]
)

# 4. Callback
@app.callback(Output("report", "children"), Input("dropDownPays", "value"))
def display_country_report(country):
    event = country
    print(event)
    if("World" in event):
        
        return country


def generateMap():
    return

if __name__ == "__main__":
    app.run_server(debug=True)


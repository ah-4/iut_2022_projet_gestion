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

feuillesExternes = [
    {
        "href": "assets/feuilleDeStyle.css",
        "rel":"stylesheet",
    },
]
app = dash.Dash(__name__,external_stylesheets=feuillesExternes)
app.title = "Outils de visualisation de données pour CafePierre"

con = sql.connect('GeoDatabase.db', check_same_thread=False)
cur = con.cursor()
cur.execute("SELECT NomPays FROM Pays")
#print(cur.fetchall())
pays = cur.fetchall()
pays = [sublist[0] for sublist in pays]
# Reading cvs file using pandas
'''df = pd.read_csv('waterLvl.csv', 
                 usecols=["crs", 
                 "total", 
                 "lat", "lon"])
df = df.rename(columns={"crs": 
                        'CRS',
                        "total": 
                        'Sea Level Rising [cm]',
                        "lat": 'Latitude',
                        "lon": 'Longitude'})'''
#Reading cvs file using pandas temperature
df = pd.read_csv('temp.csv', 
                 usecols=["crs", 
                 "TX35bc_anom", 
                 "lat", "lon"])
df = df.rename(columns={"crs": 
                        'CRS',
                        "TX35bc_anom": 
                        'Temperature raising',
                        "lat": 'Latitude',
                        "lon": 'Longitude'})

# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Creating axes and plotting world map
fig, ax = plt.subplots(figsize=(12, 6))
worldmap.plot(color="lightgrey",ax=ax,missing_kwds={'color': 'black'})

# Plotting our Impact Energy data with a color map
x = df['Longitude']
y = df['Latitude']
z = df['Temperature raising']
plt.scatter(x, y, s=20*z, c=z, alpha=0.6, vmin=-0.3, vmax=1.3,
            cmap='autumn_r')
plt.scatter(x, y, s=20*z, c=z, alpha=0.6, vmin=-5, vmax=10,
            cmap='autumn_r')
plt.colorbar(label='Montée du niveau de la mer')

# Creating axis limits and title
plt.xlim([-180, 180])
plt.ylim([-90, 90])

plt.title("La montée du niveau de la mer autour du globe")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
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
value = 0

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

image_filename = 'babyfoot.png'
cur.execute("SELECT CodePays from pays")
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
@app.callback(Output("report", "children"), Input("dropDownPays", "value"))
def display_country_report(country):
    value = country
    print(value)
    return country

if __name__ == "__main__":
    app.run_server(debug=True)


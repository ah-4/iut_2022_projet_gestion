from jupyter_dash import JupyterDash
import plotly.express as px
from dash import dcc, html, Output, Input
import pandas as pd
import sqlite3 as sql
import numpy as np
import plotly.graph_objs as go

con = sql.connect('GeoDatabase.db')
cur = con.cursor()

compare = ""
valeurPaysZone = ""
firstCountryValue = None
secondCountryValue = None
typeValue = 'PIB'
tenOrThirtyYear = 'Données sur les 10 dernières années'

requestAllValues = ("SELECT NomPays FROM Pays")
abscisseValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
requestOrdonnee = ("SELECT Valeur FROM Informer INNER JOIN Pays ON Informer.NumPays = Pays.NumPays AND Pays.NomPays = 'France' INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN 2020-10 AND 2020")
cur.execute(requestAllValues)
pays = cur.fetchall()
cur.execute(requestOrdonnee)

#abscisseValues = cur.execute(requestAbscisse)
ordonneeValues = cur.fetchall()

print(cur.fetchall())
#showRequest = pd.read_sql(requestCountryOrGeoArea, con)

pays = [sublist[0] for sublist in pays]

copiePays = pays

print("La connexion SQLite est fermée")

app = JupyterDash(__name__)
app.layout = html.Div([
    html.Div(children=[
        
        dcc.Dropdown(pays, placeholder='Choisir des pays des zones géographiques ou les deux', id='Dropdown1',multi=True),
        html.Div([], id="divTest1"),
        
        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['PIB', "Nombre d'habitants", 'Température', "Niveau de l'eau", 'Emission de CO2'],
                       'PIB', id='radioItems1'),
        html.Div([], id="divTest3"),
        
        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['Données sur les 10 dernières années', 'Données sur les 30 dernières années'], 'Données sur les 10 dernières années', id='radioItems2'),
        html.Div([], id="divTest4"),
        
        
    ], style={'padding': 10, 'flex': 1}),
    
    dcc.Graph(
        id='clientside-graph'
    ),
    dcc.Store(
        id='clientside-figure-store',
        data=[{
            'x': pays[pays['country'] == 'Canada']['year'],
            'y': pays[pays['country'] == 'Canada']['pop']
        }]
    ),
    
])

@app.callback(Output("divTest1", "children"), Input('Dropdown1', 'value'),)
def update_output(value):
    firstCountryValue = value
    
    return f'Premier pays/zone géo souhaité : {value}'

@app.callback(Output("divTest3", "children"), Input('radioItems1', 'value'),)
def update_output(value):
    typeValue = value
    if typeValue == "Nombre d'habitants":
        requestOrdonnee = ("SELECT Valeur FROM Informer INNER JOIN Pays ON Informer.NumPays = Pays.NumPays AND Pays.NomPays = {value} INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN 2020-10 AND 2020")
        cur.execute(requestOrdonnee)
        ordonneeValues = cur.fetchall()
        ordonneeValues = [sublist[0] for sublist in ordonneeValues]
        fig = go.Figure(data=[go.Scatter(x=abscisseValues, y=ordonneeValues)])
    elif typeValue == "PIB":
        requestOrdonnee = ("SELECT Valeur FROM Informer INNER JOIN Pays ON Informer.NumPays = Pays.NumPays AND Pays.NomPays = {value} INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'PIB' WHERE Annee BETWEEN 2020-10 AND 2020")
        cur.execute(requestOrdonnee)
        ordonneeValues = cur.fetchall()
        ordonneeValues = [sublist[0] for sublist in ordonneeValues]
        fig = go.Figure(data=[go.Scatter(x=abscisseValues, y=ordonneeValues)])
    elif typeValue == "Emission de CO2":
        requestOrdonnee = ("SELECT Valeur FROM Informer INNER JOIN Pays ON Informer.NumPays = Pays.NumPays AND Pays.NomPays = {value} INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'TEC' WHERE Annee BETWEEN 2020-10 AND 2020")
        cur.execute(requestOrdonnee)
        ordonneeValues = cur.fetchall()
        ordonneeValues = [sublist[0] for sublist in ordonneeValues]
        fig = go.Figure(data=[go.Scatter(x=abscisseValues, y=ordonneeValues)])
    return f'Type de valeur souhaité : {value}'

@app.callback(Output("divTest4", "children"), Input('radioItems2', 'value'),)
def update_output(value):
    tenOrThirtyYear = value
    nbAnnees = 0
    if value == 'Données sur les 10 dernières années':
        nbAnnees = 10
    else:
        nbAnnees = 30
    return f'Vous souhaitez des informations sur les {nbAnnees} dernières années'


if __name__ == '__main__':
    app.run_server(debug=True)
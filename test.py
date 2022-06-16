from jupyter_dash import JupyterDash
import plotly.express as px
from dash import dcc, html, Output, Input
import pandas as pd
import sqlite3 as sql
import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode
import matplotlib as mp
import cufflinks as cf

init_notebook_mode(connected=True)
cf.go_offline()

con = sql.connect('GeoDatabase.db')

cur = con.cursor()

compare = ""
valeurPaysZone = ""
firstCountryValue = None
secondCountryValue = None
typeValue = 'PIB'
tenOrThirtyYear = 'Données sur les 10 dernières années'

requestAllValues = ("SELECT NomPays FROM PaysImplantes")
abscisseValues = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
requestOrdonnee = ("SELECT Valeur FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays AND PaysImplantes.NomPays = 'France' INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN 2020-10 AND 2020")
world = ("SELECT NomPays FROM Pays WHERE Pays.NomPays = 'World'")
cur.execute(requestAllValues)
pays = cur.fetchall()
cur.execute(world)
pays += cur.fetchall()


#abscisseValues = cur.execute(requestAbscisse)
ordonneeValues = cur.fetchall()

print(cur.fetchall())
#showRequest = pd.read_sql(requestCountryOrGeoArea, con)

pays = [sublist[0] for sublist in pays]

copiePays = pays

df = pd.read_sql_query("SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN 2020-10 AND 2020", con)
trace = px.line(df,x="Annee",y="Valeur",title="testSARACE",color="NomPays")

app = JupyterDash(__name__)
app.layout = html.Div([
    html.Div(children=[
        
        dcc.Dropdown(pays, placeholder='Choisir des pays des zones géographiques ou les deux', id='Dropdown1',multi=True),
        html.Div([], id="divTest1"),
        
        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['PIB', "Nombre d'habitants", 'Température', "Niveau de l'eau", 'Emission de CO2'],
                       'PIB', id='radioItems1'),
        html.Div([], id="divTest2"),
        
        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['Données sur les 10 dernières années', 'Données sur les 30 dernières années'], 'Données sur les 10 dernières années', id='radioItems2'),
        html.Div([], id="divTest3"),
        
    ], style={'padding': 10, 'flex': 1}),
    
    dcc.Graph(
		id='example-graph',
		figure={
			'data': [trace],
			'layout':
			go.Layout(title='MySQL Orders Data', barmode='stack')
		}),
    
])

@app.callback(Output("divTest1", "children"), Input('Dropdown1', 'value'),)
def update_output(value):
    firstCountryValue = value[0]
    if typeValue == "Nombre d'habitants":
        requestOrdonnee = ("SELECT CONVERT(Valeur, INTEGER) FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays AND PaysImplantes.NomPays = {value} INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN CONVERT(TO_CHAR(SYSDATE, 'YYYY'), INTEGER)-10 AND CONVERT(TO_CHAR(SYSDATE, 'YYYY'), INTEGER)-2")
        cur.execute(requestOrdonnee)
        ordonneeValues = cur.fetchall()
        ordonneeValues = [sublist[0] for sublist in ordonneeValues]
        print(ordonneeValues)
    elif typeValue == "PIB":
        requestOrdonnee = ("SELECT CONVERT(Valeur, INTEGER) FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays AND PaysImplantes.NomPays = {value} INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'PIB' WHERE Annee BETWEEN CONVERT(TO_CHAR(SYSDATE, 'YYYY'), INTEGER)-10 AND CONVERT(TO_CHAR(SYSDATE, 'YYYY'), INTEGER)-2")
        cur.execute(requestOrdonnee)
        ordonneeValues = cur.fetchall()
        ordonneeValues = [sublist[0] for sublist in ordonneeValues]
        print(ordonneeValues)
    elif typeValue == "Emission de CO2":
        requestOrdonnee = ("SELECT CONVERT(Valeur, INTEGER) FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays AND PaysImplantes.NomPays = {value} INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'TEC' WHERE Annee BETWEEN CONVERT(TO_CHAR(SYSDATE, 'YYYY'), INTEGER)-10 AND CONVERT(TO_CHAR(SYSDATE, 'YYYY'), INTEGER)-2")
        cur.execute(requestOrdonnee)
        ordonneeValues = cur.fetchall()
        ordonneeValues = [sublist[0] for sublist in ordonneeValues]
        print(ordonneeValues)
    return f'Premier pays/zone géo souhaité : {value}'

@app.callback(Output("divTest2", "children"), Input('radioItems1', 'value'),)
def update_output(value):
    typeValue = value
    
    return f'Type de valeur souhaité : {value}'

@app.callback(Output("divTest3", "children"), Input('radioItems2', 'value'),)
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
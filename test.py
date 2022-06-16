from gc import callbacks
from jupyter_dash import JupyterDash
import plotly.express as px
from dash import dcc, html, Output, Input
import pandas as pd
import sqlite3 as sql
import numpy as np
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode
import matplotlib as mp


con = sql.connect('GeoDatabase.db',check_same_thread=False)

cur = con.cursor()

compare = ""
valeurPaysZone = ""
firstCountryValue = None
secondCountryValue = None
typeValue = 'PIB'
tenOrThirtyYear = 'Données sur les 10 dernières années'

'''Remplissage de la liste des pays'''
requestAllValues = ("SELECT NomPays FROM PaysImplantes")
requestOrdonnee = ("SELECT Valeur FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays AND PaysImplantes.NomPays = 'France' INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN 2020-10 AND 2020")
world = ("SELECT NomPays FROM Pays WHERE Pays.NomPays = 'World'")
cur.execute(requestAllValues)
pays = cur.fetchall()
cur.execute(world)
pays += cur.fetchall()
pays = [sublist[0] for sublist in pays]
listePays = None

requestPIB = "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'PIB'"
requestNbPop = "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION'"
requestTemp = "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'P'"
requestCarbon= "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'TEC'"
requestActuelle = requestPIB
plageTemps = "WHERE Annee BETWEEN 2020-10 AND 2020"
plagePays = " AND NomPays IN "
nbAnnees = 10
titreGraph = "Evolution de la population"

app = JupyterDash(__name__)
app.layout = html.Div([
    html.Div(children=[
        
        dcc.Dropdown(pays, placeholder='Choisir des pays des zones géographiques ou les deux', id='Dropdown1',multi=True),
        html.Div([], id="divTest1"),
        
        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['PIB', "Nombre d'habitants", 'Emission de CO2'],
                       'PIB', id='radioItems1'),
        html.Div([], id="divTest2"),
        
        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['Données sur les 10 dernières années', 'Données sur les 30 dernières années'], 'Données sur les 10 dernières années', id='radioItems2'),
        html.Div([], id="divTest3"),
        
        html.Br(),
        html.Button('Evolution de la température mondiale', id='btn-nclicks-1', style={'backgroundColor':'transparent',
                                                                                       'height':30, 'font-size':20}),
        html.Br(),
        html.Br(),
        html.Button('Evolution de la montée des eaux mondiale', id='btn-nclicks-2', style={'backgroundColor':'transparent',
                                                                                           'height':30, 'font-size':20}),
        
    ], style={'padding': 10, 'flex': 1}),
    html.Div(children=None,hidden=True,id="rangement"),
    dcc.Graph(
		id='example-graph')    
])

@app.callback(Output("example-graph", "figure"), Input('radioItems1', 'value'),Input('radioItems2', 'value'),Input("Dropdown1",'value'))
def update_output(radioItems1,radioItems2,Dropdown1):
    listePays = Dropdown1
    lasainteString = '('
    if listePays != None :
        for pays in enumerate(listePays):
            p = pays[1].replace("'", "''")
            lasainteString += "'"+p+"',"
    lasainteString = lasainteString[0:len(lasainteString)-1] + ')'
    print(lasainteString)
    if radioItems2 == 'Données sur les 10 dernières années':
        plageTemps = " WHERE Annee BETWEEN 2020-10 AND 2020"
    else :
        plageTemps = " WHERE Annee BETWEEN 2020-30 AND 2020"
    if radioItems1 == "Nombre d'habitants":
        requestActuelle = requestNbPop
        titreGraph = "Evolution du nombre d'habitants"
    elif radioItems1 == "PIB":
        requestActuelle = requestPIB
        titreGraph = "Evolution du PIB"
    elif radioItems1 == "Emission de CO2":
        requestActuelle = requestCarbon
        titreGraph = "Evolution des émissions de CO2"
    if(listePays != None):
        df = pd.read_sql_query(str(requestActuelle+" "+plageTemps+plagePays+lasainteString),con)
    else :
        df = df = pd.read_sql_query(str(requestActuelle+" "+plageTemps),con)
    trace = px.line(df,x="Annee",y="Valeur",title=titreGraph,color="NomPays",markers=True,labels={"NomPays":"Nom des pays"}, height=700)
    return trace

@app.callback(Output("divTest3", "children"), Input('radioItems2', 'value'),)
def update_output(value):
    if value == 'Données sur les 10 dernières années':
        nbAnnees = 10
    else:
        nbAnnees = 30
    return f'Vous souhaitez des informations sur les {nbAnnees} dernières années'
@app.callback(Output("rangement","children"),Input("Dropdown1",'value'))
def reqListePays(value):
    listePays = value
    return listePays
if __name__ == '__main__':
    app.run_server(debug=True)
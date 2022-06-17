from contextlib import nullcontext
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
import base64


con = sql.connect('GeoDatabase.db',check_same_thread=False)
cur = con.cursor()
# external CSS stylesheets
external_stylesheets = ['assets/feuilleDeStyle.css']

imgLoad =None
refreshed = 0
imgChosen = [None for i in range(3)]
lastButtonId = None
buttonOff = {'backgroundColor':'transparent','height':30, 'font-size':20}
buttonOn = {'backgroundColor':'white','height':30, 'font-size':20}
cartes=""
compare = ""
valeurPaysZone = ""
firstCountryValue = None
secondCountryValue = None
typeValue = 'PIB'
tenOrThirtyYear = 'Données sur les 10 dernières années'

cur.execute("SELECT Annee FROM Repartir INNER JOIN PaysImplantes ON Repartir.NumPays = PaysImplantes.NumPays ")
annees = cur.fetchall()
annees = [sublist[0] for sublist in annees]

'''Remplissage de la liste des pays'''
requestAllValues = ("SELECT NomPays FROM PaysImplantes")
requestOrdonnee = ("SELECT Valeur FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays AND PaysImplantes.NomPays = 'France' INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN 2020-10 AND 2020")
world = ("SELECT NomPays FROM Pays WHERE Pays.NomPays = 'World'")
cur.execute(requestAllValues)
pays = cur.fetchall()
cur.execute(world)
pays += cur.fetchall()
pays = [sublist[0] for sublist in pays]

requestPIB = "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'PIB'"
requestNbPop = "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION'"
requestTemp = "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'P'"
requestCarbon= "SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'TEC'"
requestActuelle = requestPIB
plageTemps = "WHERE Annee BETWEEN 2020-10 AND 2020"
plagePays = " AND NomPays IN "
nbAnnees = 10
app = JupyterDash(__name__,external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div(className = "total",children=[
        
        dcc.Dropdown(pays, placeholder='Choisir des pays des zones géographiques ou les deux', id='Dropdown1',multi=True),
        html.Div([], id="divTest1"),
        html.Div(className="firstPart",children=[
            html.Br(),
            html.Label('Sélectionnez le type de données que vous souhaitez visualiser :'),
            dcc.RadioItems(['PIB', "Nombre d'habitants", 'Emission de CO2'],
                        'PIB', id='radioItems1',className="sus"),
            
            html.Br(),
            html.Label("Sélectionnez l'échelle de temps :"),
            dcc.RadioItems(['Données sur les 10 dernières années', 'Données sur les 30 dernières années'], 'Données sur les 10 dernières années', id='radioItems2'),
            html.Div([], id="divTest3"),
            
            html.Br(),
            html.Button('Evolution de la température mondiale', id='temp', style={'backgroundColor':'transparent','height':30, 'font-size':20}),
            html.Br(),
            html.Br(),
            html.Button('Evolution de la montée des eaux mondiale', id='water', style={'backgroundColor':'transparent','height':30, 'font-size':20}),
            html.Br(),
            html.Br(),
            html.Button('Evolution des émissions de carbone mondiale', id='carbone', style={'backgroundColor':'transparent','height':30, 'font-size':20}),
            html.Br(),
        ]),
        html.Img(src="", n_clicks=0,id="imgCartes", style={'display':'None'}),
        
        html.Div("",  style={'display':'None'})
        
    ], style={'padding': 10, 'flex': 1}),
    html.Div(children=None,hidden=True,id="rangement"),
    dcc.Graph(
		id='example-graph')  ,
    html.Br(),
    dcc.RadioItems(['Part mondiale', 'Secteurs emission'],'Part mondiale', id='radioCircle'),
    dcc.Dropdown(annees, placeholder="Choisissez l'année recherchée :",value=2020, id='DropdownAnnee'),
    dcc.Dropdown(pays, placeholder="Choisissez le Pays à analyser recherchée :", id='DropdownPays'),
    dcc.Graph(
		id='radius-graph')  
])


@app.callback(Output("radius-graph", "figure"), Input('radioCircle', 'value'),Input("DropdownAnnee",'value'),Input("DropdownPays",'value'))
def update_output(value1,value2,pays):   
    if(value1 == "Part mondiale"):
        df = pd.read_sql_query("SELECT * FROM Repartir INNER JOIN PaysImplantes ON Repartir.NumPays = PaysImplantes.NumPays INNER JOIN Secteur ON Secteur.NumSecteur = Repartir.NumSecteur WHERE Secteur.NumSecteur = 6 AND Repartir.Annee = " + str(value2),con)
        fig = px.pie(df, values="Valeur", names="NomPays") 
    elif pays != None :
        df = pd.read_sql_query("SELECT Valeur,NomSecteur FROM Repartir INNER JOIN PaysImplantes ON Repartir.NumPays = PaysImplantes.NumPays INNER JOIN Secteur ON Secteur.NumSecteur = Repartir.NumSecteur WHERE Secteur.NumSecteur != 6 AND Repartir.Annee = " + str(value2) + " AND PaysImplantes.NomPays = '" +str(pays)+"'",con)
        fig = px.pie(df, values="Valeur", names="NomSecteur") 
    else:
        print("Choisissez un pays")
        df = pd.read_sql_query("SELECT * FROM Repartir INNER JOIN PaysImplantes ON Repartir.NumPays = PaysImplantes.NumPays INNER JOIN Secteur ON Secteur.NumSecteur = Repartir.NumSecteur WHERE Secteur.NumSecteur = 6 AND Repartir.Annee = " + str(value2),con)
        fig = px.pie(df, values="Valeur", names="NomPays") 
    return fig

    
@app.callback(Output("example-graph", "figure"), Input('radioItems1', 'value'),Input('radioItems2', 'value'),Input("Dropdown1",'value'))
def update_output(radioItems1,radioItems2,Dropdown1):
    listePays = Dropdown1
    lasainteString = ''
    if listePays != None :
        lasainteString = '('
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
        legende = "Nombre d'habitants"
    elif radioItems1 == "PIB":
        requestActuelle = requestPIB
        titreGraph = "Evolution du PIB"
        legende = "Valeure du PIB (T = Trillion)"
    elif radioItems1 == "Emission de CO2":
        requestActuelle = requestCarbon
        titreGraph = "Evolution des émissions de CO2"
        legende = "Emmissions de CO2 en tonnes"
    if(listePays != None and listePays != []):
        df = pd.read_sql_query(str(requestActuelle+" "+plageTemps+plagePays+lasainteString),con)
    else :
        df = df = pd.read_sql_query(str(requestActuelle+" "+plageTemps),con)
    trace = px.line(df,x="Annee",y="Valeur",title=titreGraph,color="NomPays",markers=True,labels={"NomPays":"Nom des pays","Valeur":legende}, height=700)
    return trace

@app.callback(Output("divTest3", "children"), Input('radioItems2', 'value'))
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

@app.callback(Output("imgCartes", "src"), Output("imgCartes", "style"),Output("temp","style"),Output("water","style"), Output("carbone","style"),  Input("temp", "n_clicks"), Input("water", "n_clicks"), Input("carbone", "n_clicks"))
def update_output(valueTemp, valueWater, valueCarbone):
    global imgLoad, imgChosen, refreshed,lastButtonId
    
    choice = [valueTemp, valueWater, valueCarbone]
    tempStyle = waterStyle = carboneStyle = buttonOff
    changedI = 0
    for i in range(3):
        changedI = i
        if choice[i] != imgChosen[i]:
            break
    if changedI == 0:
        imgLoad = 'mapTemp.png'
        tempStyle = buttonOn
    elif changedI == 1:
        imgLoad = 'levelMap.png'
        waterStyle = buttonOn
    elif changedI == 2:
        imgLoad = 'mapCO2.png'
        carboneStyle = buttonOn
    
    refreshed += 1
    s = {'display': 'block'}
    print(lastButtonId)
    if refreshed <= 1 or lastButtonId == changedI:
        s = {'display': 'None'}
        lastButtonId = None
        tempStyle = waterStyle = carboneStyle = buttonOff
    else :
        lastButtonId = changedI
    imgChosen = choice
    return app.get_asset_url(imgLoad), s,tempStyle,waterStyle,carboneStyle


if __name__ == '__main__':
    app.run_server(debug=True)
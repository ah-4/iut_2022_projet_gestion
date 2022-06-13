from jupyter_dash import JupyterDash
import plotly.express as px
from dash import dcc, html, Output, Input
import pandas as pd
import sqlite3 as sql

a = "toto"
con = sql.connect('GeoDatabase.db')
cur = con.cursor()
print("Base de données créée et correctement connectée à SQLite")

cur.execute("SELECT NomPays FROM Pays")
toto = cur.fetchall()

cur.close()
con.close()
print("La connexion SQLite est fermée")

toto2 = []

for country in toto:
    toto2.append(country)
    
print(toto2)

'''df = pd.DataFrame({
    "Temps": toto2,
    "Pays": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app = JupyterDash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Test de Dash HTML", style={'color' : 'red'}),
        dcc.Dropdown(
            placeholder='Choose a country', id='demo-dropdown',
            options = [{"label" : pays, "value" : pays} for pays in toto],
            value=toto[0][0]
        ),
        
        dcc.Graph(
        id='example-graph',
        figure=fig
    )
    ]
)

@app.callback(
    Output("", ""),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    a = value
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server()
    
    '''
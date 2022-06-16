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
cur.execute("SELECT NomPays, Valeur, Annee FROM Informer INNER JOIN PaysImplantes ON Informer.NumPays = PaysImplantes.NumPays INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee AND TypeDonnee.NomTypeDonnee = 'NB_POPULATION' WHERE Annee BETWEEN 2020-30 AND 2020")
print(cur.fetchall())
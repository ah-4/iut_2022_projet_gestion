import sqlite3 as sql
import plotly.express as px 
import pandas as pd
con = sql.connect('GeoDatabase.db',check_same_thread=False)
cur = con.cursor()
#cur.execute("SELECT * FROM Secteur")
#print(cur.fetchall())

cur.execute("SELECT Valeur,NomSecteur FROM Repartir INNER JOIN PaysImplantes ON Repartir.NumPays = PaysImplantes.NumPays INNER JOIN Secteur ON Secteur.NumSecteur = Repartir.NumSecteur WHERE Annee = 2015 AND PaysImplantes.NomPays = 'France'")
print(cur.fetchall()) 

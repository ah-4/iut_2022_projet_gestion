import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd


#Reading cvs file using pandas temperature
df = pd.read_csv('temperatureMoyenne.csv', 
                usecols=["crs", 
                "tas_anom", 
                "lat", "lon"])
df = df.rename(columns={"crs": 
                        'CRS',
                        "tas_anom": 
                        'Temperature raising',
                        "lat": 'Latitude',
                        "lon": 'Longitude'})

# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Creating axes and plotting world map
fig, ax = plt.subplots(figsize=(12, 6))
worldmap.boundary.plot(ax=ax,edgecolor="black")

# Plotting our Impact Energy data with a color map
x = df['Longitude']
y = df['Latitude']
z = df['Temperature raising']
plt.scatter(x, y, s=1*z, c=z, alpha=0.6, vmin=-1, vmax=+10,
            cmap='autumn_r')
plt.colorbar(label='Evolution de la température')

# Creating axis limits and title
plt.xlim([-180, 180])
plt.ylim([-90, 90])

plt.title("L'évolution de la température autour du globe")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("mapTemp.png")
 # Reading cvs file using pandas
df = pd.read_csv('waterLvl.csv', 
                usecols=["crs", 
                "total", 
                "lat", "lon"])
df = df.rename(columns={"crs": 
                        'CRS',
                        "total": 
                        'Sea Level Rising [cm]',
                        "lat": 'Latitude',
                        "lon": 'Longitude'})
# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Creating axes and plotting world map
fig, ax = plt.subplots(figsize=(12, 6))
worldmap.boundary.plot(ax=ax,edgecolor="black")

# Plotting our Impact Energy data with a color map
x = df['Longitude']
y = df['Latitude']
z = df['Sea Level Rising [cm]']
plt.scatter(x, y, s=20*z, c=z, alpha=0.6, vmin=-0.4, vmax=1.5,
            cmap='Blues')
plt.colorbar(label='Montee du niveau de la mer')

# Creating axis limits and title
plt.xlim([-180, 180])
plt.ylim([-90, 90])

plt.title("La montée du niveau de la mer autour du globe")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("levelMap.png")

#Reading cvs file using pandas temperature
df = pd.read_csv('temperatureMoyenne.csv', 
                usecols=["crs", 
                "tas_anom", 
                "lat", "lon"])
df = df.rename(columns={"crs": 
                        'CRS',
                        "tas_anom": 
                        'Temperature raising',
                        "lat": 'Latitude',
                        "lon": 'Longitude'})

# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Creating axes and plotting world map
fig, ax = plt.subplots(figsize=(12, 6))
worldmap.boundary.plot(ax=ax,edgecolor="black")

# Plotting our Impact Energy data with a color map
x = df['Longitude']
y = df['Latitude']
z = df['Temperature raising']
plt.scatter(x, y, s=1*z, c=z, alpha=0.6, vmin=-1, vmax=+10,
            cmap='autumn_r')
plt.colorbar(label='Evolution de la température')

# Creating axis limits and title
plt.xlim([-180, 180])
plt.ylim([-90, 90])

plt.title("L'évolution de la température autour du globe")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("mapTemp.png")


 # Reading cvs file using pandas
df = pd.read_csv('waterLvl.csv', 
                usecols=["crs", 
                "total", 
                "lat", "lon"])
df = df.rename(columns={"crs": 
                        'CRS',
                        "total": 
                        'Sea Level Rising [cm]',
                        "lat": 'Latitude',
                        "lon": 'Longitude'})
# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Creating axes and plotting world map
fig, ax = plt.subplots(figsize=(12, 6))
worldmap.boundary.plot(ax=ax,edgecolor="black")

# Plotting our Impact Energy data with a color map
x = df['Longitude']
y = df['Latitude']
z = df['Sea Level Rising [cm]']
plt.scatter(x, y, s=20*z, c=z, alpha=0.6, vmin=-0.4, vmax=1.5,
            cmap='Blues')
plt.colorbar(label='Montee du niveau de la mer')

# Creating axis limits and title
plt.xlim([-180, 180])
plt.ylim([-90, 90])

plt.title("La montée du niveau de la mer autour du globe")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("levelMap.png")

#Reading cvs file using pandas temperature
df = pd.read_csv('actualCO2.csv', 
                usecols=["crs", 
                "co2", 
                "lat", "lon"])
df = df.rename(columns={"crs": 
                        'CRS',
                        "co2": 
                        'CO2',
                        "lat": 'Latitude',
                        "lon": 'Longitude'})

# From GeoPandas, our world map data
worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Creating axes and plotting world map
fig, ax = plt.subplots(figsize=(12, 6))
worldmap.boundary.plot(ax=ax,edgecolor="black")

# Plotting our Impact Energy data with a color map
x = df['Longitude']
y = df['Latitude']
z = df['CO2']
plt.scatter(x, y, s=1*z, c=z, alpha=0.6, vmin=-5, vmax=5,
            cmap='autumn_r')
plt.colorbar(label='Quantité de CO2 émise')

# Creating axis limits and title
plt.xlim([-180, 180])
plt.ylim([-90, 90])

plt.title("L'emission de CO2 autour du globe")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("mapCO2.png")
"""
    Database generator script
    @author Team 5 with: Giovanni Ahite, Ali Ozturk, Benjamin Gandelin, Damien Richard & Loïc Lévêque
"""

# Dependencies
from builtins import print

import pandas as pd
import sqlite3
import os

# Constants
DEBUG = False  # If true, log messages will be displayed for mostly each request

LAST_YEAR = 2021
FIRST_YEAR = LAST_YEAR - 30

DATA_TYPES = ('NB_POPULATION', 'PIB', 'TEC')
SECTORS = ('CIMENT', 'CHARBON', 'GAZ', 'HUILE', 'AUTRES', 'PART_MONDIAL')

CONTINENTS_FILEPATH = "data/continent_country.csv"

COUNTRIES_GDP_FILEPATH = "data/countries_gdp.xls"  # Excel file path for GDP per inhabitant per country
COUNTRIES_GDP_COLUMN_NAMES_LINE_INDEX = 2  # Line for information (Country Name, Years...)
COUNTRIES_GDP_VALUES_START_INDEX = COUNTRIES_GDP_COLUMN_NAMES_LINE_INDEX + 1  # First line of datas

COUNTRIES_CO2_FILEPATH = "data/countries_co2.xls"  # Excel file path for CO2 emissions per country
COUNTRIES_CO2_COLUMN_NAMES_LINE_INDEX = 2  # Line for information (Country Name, Years...)
COUNTRIES_CO2_VALUES_START_INDEX = COUNTRIES_CO2_COLUMN_NAMES_LINE_INDEX + 1  # First line of datas

COUNTRIES_POP_FILEPATH = "data/countries_population.xls"  # Excel file path for CO2 emissions per country
COUNTRIES_POP_COLUMN_NAMES_LINE_INDEX = 2  # Line for information (Country Name, Years...)
COUNTRIES_POP_VALUES_START_INDEX = COUNTRIES_POP_COLUMN_NAMES_LINE_INDEX + 1  # First line of datas

COUNTRIES_CO2_PER_SECTOR = "data/countries_co2_data.xls"

DATABASE_OUT_PATH = 'GeoDatabase.db'  # Database output file path

# Objects
con = None  # Database connection
cursor = None  # Database cursor


def log(message):
    """
    Log the message, if DEBUG is True
    :param message: the message
    """
    if DEBUG:
        print(message)


def init_db_conn():
    """
    Initialize database connection
    """
    global con, cursor

    if os.path.exists(DATABASE_OUT_PATH):
        os.remove(DATABASE_OUT_PATH)

    con = sqlite3.connect(DATABASE_OUT_PATH)
    cursor = con.cursor()
    print("Connected to database! Filepath:", DATABASE_OUT_PATH)


def _sql_foreign_key(key, referenced_table, referenced_key):
    """
    Return the SQL column for a foreign key
    :return: column
    """
    return "FOREIGN KEY ({}) REFERENCES {}({})".format(key, referenced_table, referenced_table)


def _sql_request_create_table(name, columns):
    """
    Return the SQL request for a table creation with specified parameters
    :param name: table name
    :param columns: table columns
    :return: request
    """
    lines = "CREATE TABLE {}(\n".format(name)
    arrays_length = len(columns)
    i = 0
    for c in columns:
        lines += c + ("" if i == arrays_length - 1 else ",") + "\n"
        i += 1
    lines += ");"
    return lines


def _sql_request_insert_into(table, values):
    """
    Return the request for inserting values into the table
    :param table: table name
    :param values: dict as key: value
    :return: request
    """
    columns = "("
    affected_values = "("
    i, keys_length = 0, len(values.keys())
    for column in values.keys():
        comma = (", " if i != keys_length - 1 else "")
        columns += column + comma
        value = values[column]
        if type(value) == str:
            value = value.replace("'", "''")
            value = "'{}'".format(value)
        affected_values += str(value) + comma
        i += 1
    columns += ")"
    affected_values += ")"
    request = "INSERT INTO {}{} VALUES {};".format(table, columns, affected_values)
    log(request)
    return request


def _sql_query(query, args=()):
    """
    Request query to the database, then fetch and return result rows.
    :param query: the request
    :return: rows
    """
    if len(args) == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    rows = cursor.fetchall()
    return rows


def init_tables():
    """
    Create database tables
    """
    # Geographical zone table
    tables_args = {
        "GeographicalZone": (
            "ZoneGeographique",
            (
                "NumZoneGeo INTEGER PRIMARY KEY AUTOINCREMENT",
                "NomZoneGeo TEXT NOT NULL"
            )
        ),
        "Country": (
            "Pays",
            (
                "NumPays INTEGER PRIMARY KEY AUTOINCREMENT",
                "NomPays TEXT NOT NULL",
                "CodePays TEXT NOT NULL",
                "NumZoneGeo INTEGER NOT NULL",
                _sql_foreign_key("NumZoneGeo", "ZoneGeographique", "NumZoneGeo"),
                "UNIQUE(CodePays)",
                "UNIQUE(NomPays)"
            )
        ),
        "DataType": (
            "TypeDonnee",
            (
                "NumTypeDonnee INTEGER PRIMARY KEY AUTOINCREMENT",
                "NomTypeDonnee TEXT NOT NULL UNIQUE"
            )
        ),
        "Inform": (
            "Informer",
            (
                "NumPays INTEGER NOT NULL",
                "NumTypeDonnee INTEGER NOT NULL",
                "Valeur REAL",
                "Annee INTEGER NOT NULL",
                _sql_foreign_key("NumPays", "Pays", "NumPays"),
                _sql_foreign_key("NumTypeDonnee", "TypeDonnee", "NumTypeDonnee"),
                "UNIQUE(NumPays, NumTypeDonnee, Annee)"
            )
        ),
        "Sector": (
            "Secteur",
            (
                "NumSecteur INTEGER PRIMARY KEY AUTOINCREMENT",
                "NomSecteur TEXT NOT NULL UNIQUE"
            )
        ),
        "Part": (
            "Repartir",
            (
                "NumPays INTEGER NOT NULL",
                "NumSecteur INTEGER NOT NULL",
                "Valeur REAL",
                "Annee INTEGER NOT NULL",
                _sql_foreign_key("NumPays", "Pays", "NumPays"),
                _sql_foreign_key("NumSecteur", "Secteur", "NumSecteur"),
                "UNIQUE(NumPays, NumSecteur, Annee)"
            )
        )
    }
    for t_key in tables_args.keys():
        table = tables_args[t_key]
        request = _sql_request_create_table(table[0], table[1])
        log("Initializing table {}...".format(t_key))
        cursor.execute(request)
        log("Table {} has been initialized!".format(t_key))


def _get_countries_by_continents():
    """
    Return all continents and its associated countries
    :return: CTN, [COUNTRIES CODE]
    """
    df = pd.read_csv(CONTINENTS_FILEPATH)
    df.drop(columns=['Continent_Code', 'Two_Letter_Country_Code', 'Country_Number', 'Country_Name'], axis=0)
    g = df.groupby(['Continent_Name'])
    return g


def fill_geo_zones():
    """
    Insert geographical zones into the database
    """
    g = _get_countries_by_continents()
    for data_df in g:
        continent = data_df[0]
        request = _sql_request_insert_into("ZoneGeographique", {"NomZoneGeo": continent})
        cursor.execute(request)
        log("Geographical Zone {} has been inserted!".format(continent))


def fill_countries():
    """
    Fulfill countries
    """
    df = pd.read_excel(COUNTRIES_GDP_FILEPATH)
    info_line = df.iloc[COUNTRIES_GDP_COLUMN_NAMES_LINE_INDEX].to_list()
    country_name_id = info_line.index('Country Name')
    country_code_id = info_line.index('Country Code')
    i = COUNTRIES_GDP_VALUES_START_INDEX
    while df.loc[i][country_name_id] != "":
        data_line = df.loc[i]
        country_name = data_line[country_name_id]
        country_code = data_line[country_code_id]
        request = _sql_request_insert_into("Pays", {"NomPays": country_name, "CodePays": country_code, "NumZoneGeo": 0})
        cursor.execute(request)
        log("Country {} ({}) inserted!".format(country_name, country_code))
        i += 1
        try:
            df.loc[i][country_name_id] != ""
        except Exception:
            break
    g = _get_countries_by_continents()
    for data_df in g:
        continent = data_df[0]
        for country_code in data_df[1]['Three_Letter_Country_Code'].values:
            _sql_query("UPDATE Pays SET NumZoneGeo = (SELECT ZoneGeographique.NumZoneGeo FROM ZoneGeographique WHERE NomZoneGeo = '{}') WHERE CodePays = '{}'".format(continent, country_code))
            log("Country {} has been associated with the continent of {}".format(country_code, continent))


def _fill_type(values, table_name, column_name):
    """
    FIll the requested table with values.
    :param values: Values to insert
    :param table_name: Table name
    :param column_name: Column name
    """
    for data_type in values:
        request = _sql_request_insert_into(table_name, {column_name: data_type})
        cursor.execute(request)
        log("Data type ({}) {} has been inserted!".format(table_name, data_type))


def fill_data_types():
    """
    Insert data types into the database
    """
    _fill_type(DATA_TYPES, "TypeDonnee", "NomTypeDonnee")
    _fill_type(SECTORS, "Secteur", "NomSecteur")


def init_default_tables():
    """
    Fulfill Countries and Geographical Zones tables
    """
    fill_data_types()
    fill_geo_zones()
    fill_countries()


def fetch_country_usual_data(xls_file, info_line_index, first_data_line_index, data_type):
    """
    Insert each country GDP into the database
    """
    # Open GDP file
    df = pd.read_excel(xls_file)

    # Info line and initialization
    info_line = df.loc[info_line_index].to_list()
    years = {}
    country_code_id = info_line.index('Country Code')

    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        years[year] = info_line.index(year)

    # Loop to fetch datas
    i = first_data_line_index
    while df.loc[i][country_code_id] != "":
        data_line = df.loc[i]
        country_code = data_line[country_code_id]
        country_id = _sql_query("SELECT NumPays FROM Pays WHERE CodePays = '{}'".format(country_code))[0][0]
        data_type_id = _sql_query("SELECT NumTypeDonnee FROM TypeDonnee WHERE NomTypeDonnee = '{}'".format(data_type))[0][0]
        for year in range(FIRST_YEAR, LAST_YEAR + 1):
            value = data_line[years[year]]
            if str(value).lower() in ("nan", ""):
                continue
            request = _sql_request_insert_into("Informer", {"NumPays": country_id, "NumTypeDonnee": data_type_id, "Annee": year,
                                                  "Valeur": value})
            cursor.execute(request)
            log("The value for the country with code ({}) has been inserted for data type {} in {}: {}".format(
                country_code, data_type, year, value))
        i += 1
        try:
            df.loc[i][country_code_id] != ""
        except Exception:
            break


def fetch_co2_per_country():
    """
    Fetch CO2 per sector per country
    """

    info_columns = (
        "iso_code",
        "year"
    )

    data_columns = ("cement_co2",
        "coal_co2",
        "gas_co2",
        "oil_co2",
        "other_industry_co2",
        "share_global_co2")

    fixed_columns = {}
    for i in range(len(data_columns)):
        fixed_columns[data_columns[i]] = SECTORS[i]

    df = pd.read_excel(COUNTRIES_CO2_PER_SECTOR)
    df = df[list(info_columns + data_columns)]
    for data in df.itertuples(False):
        country_code = str(data.iso_code)
        if country_code == 'nan':
            continue
        year = data.year
        for fixed_column, sector_name in fixed_columns.items():
            value = data[len(info_columns) + data_columns.index(fixed_column)]
            if str(value) == 'nan':
                continue
            sector_id = _sql_query("SELECT NumSecteur FROM Secteur WHERE NomSecteur = '{}'".format(sector_name))[0][0]
            try:
                country_id = _sql_query("SELECT NumPays FROM Pays WHERE CodePays = '{}'".format(country_code))[0][0]
            except Exception:
                continue
            request = _sql_request_insert_into("Repartir",
                                               {"NumPays": country_id, "NumSecteur": sector_id, "Annee": year,
                                                "Valeur": value})
            con.execute(request)
            log("Part of {} in country {} has been added! ({})".format(fixed_column, country_code, value))


def fetch_datas():
    """
    Fetch all datas for each data type
    """
    fetch_country_usual_data(COUNTRIES_GDP_FILEPATH, COUNTRIES_GDP_COLUMN_NAMES_LINE_INDEX, COUNTRIES_GDP_VALUES_START_INDEX, "PIB")
    fetch_country_usual_data(COUNTRIES_CO2_FILEPATH, COUNTRIES_CO2_COLUMN_NAMES_LINE_INDEX, COUNTRIES_CO2_VALUES_START_INDEX, "TEC")
    fetch_country_usual_data(COUNTRIES_POP_FILEPATH, COUNTRIES_POP_COLUMN_NAMES_LINE_INDEX, COUNTRIES_POP_VALUES_START_INDEX, "NB_POPULATION")
    fetch_co2_per_country()


def fulfill_database():
    """
    Fetch data from source files then fill the tables into database.
    """
    init_default_tables()
    fetch_datas()


def tests():
    """
    Print all test results
    """
    print("Tests:")

    print("Test get countries:")
    print(_sql_query("SELECT * FROM Pays"))

    print("Test ID selections:")
    data_type_id = _sql_query("SELECT NumTypeDonnee FROM TypeDonnee WHERE NomTypeDonnee = 'NB_POPULATION'")[0][0]
    country_id = _sql_query("SELECT NumPays FROM Pays WHERE CodePays = 'ZWE'")[0][0]
    print(data_type_id, country_id)

    print("Test selection USA on all data types:")
    request = \
        """
        SELECT Valeur, NomTypeDonnee FROM Informer
        INNER JOIN Pays ON Informer.NumPays = Pays.NumPays AND Pays.CodePays = 'USA'
        INNER JOIN TypeDonnee ON Informer.NumTypeDonnee = TypeDonnee.NumTypeDonnee
        WHERE ANNEE = 2018;
        """
    print(request)
    print(_sql_query(request))

    print("Test selection USA on all data types:")
    request = \
        """
        SELECT Valeur, NomSecteur FROM Repartir
        INNER JOIN Pays ON Repartir.NumPays = Pays.NumPays AND Pays.CodePays = 'USA'
        INNER JOIN Secteur ON Repartir.NumSecteur = Secteur.NumSecteur
        WHERE ANNEE = 2016;
        """
    print(request)
    print(_sql_query(request))


def main():
    """
    Main entry function
    """
    init_db_conn()
    if con is None:
        print("Connection to database has failed! Exit...")
        return
    init_tables()
    fulfill_database()
    tests()
    if con is not None:
        con.commit()
        con.close()
        print("Connection to database closed!")


main()

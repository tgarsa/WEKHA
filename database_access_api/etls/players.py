# Load the data into the Silver Layer.

# Necessary imports
import pandas as pd
# Access to our how Library
from utils import database, network, time
import normalize

# Access to the PostgresSQL database
import psycopg2
from numpy import int64
# from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(int64, psycopg2.extensions.AsIs)

# Define the connection
# We won't close because we will need to continued using.
connection = psycopg2.connect(
    host=network.ip,
    port=5432,
    database=database.database,
    user=database.user,
    password=database.password
)


def add(player):

    # Access to the database
    cursor = connection.cursor()
    # Define SQL to insert the data.
    # Write into the bronze table
    sql = "INSERT INTO jugadores (id_jugador, dni, nombre, apellidos, nick, email, telefono, residencia, talla, "\
          "discapacidades, observaciones, created_at, updated_at) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for cont in range(player.shape[0]):
        data = player.iloc[cont]
        # Now, we build the internal data, "updated_at", and "created_at"
        data['created_at'] = time.now()
        data['updated_at'] = data['created_at']

        # Now we clean the data to have the most correct estructure
        df = normalize.normalize(df)
        cursor.execute(sql, (data['id_jugador'], data['dni'], data['nombre'], data['apellidos'], data['nick'],
                             data['email'], data['telefono'], data['residencia'], data['talla'],
                             data['discapacidades'], data['observaciones'], data['created_at']))
        # Commit the data
        connection.commit()

    # cursor
    # connection.close()
    return 'Added to Silver layer.'

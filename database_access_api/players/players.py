
# Access to the PostgreSQL database

import psycopg2
import numpy as np
from pandas import notnull
from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int64, AsIs)

from database_access_api.utils import network, database

conexion = psycopg2.connect(
    host= network.ip,
    port=5432,
    database=database.database,
    user=database.user,
    password=database.password
)


def _set(player):
    '''
    We save the data of the player in to the database.
    In this case only one player.
    This is a first approach, I will need to define the function to build the ID
    :param player: DataFrame/Dictionary with the data of the player.
    :return:
    '''

    # Access to the database
    cursor = conexion.cursor()

    # Define SQL to insert the data.
    sql = "INSERT INTO jugadores (id_jugador, dni, nombre, apellidos, nick, email, telefono, talla, discapacidades, "\
          "observaciones) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # To don't have a problem if observaciones in empty
    if notnull(player['observaciones']):
        observaciones = player['observaciones']
    else:
        observaciones = ""

    id_jugador = 'PEPOTE'

    cursor.execute(sql, (id_jugador, player['dni'], player['nombre'], player['apellidos'], player['nick'],
                         player['email'], player['telefono'], player['talla'], player['discapacidades'], observaciones))

    conexion.commit()
    return {"label": 'It done'}

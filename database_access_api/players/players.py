# Access to the Library
from utils import database, network

# Access to the PostgreSQL database
import psycopg2
from numpy import int64

from psycopg2.extensions import register_adapter, AsIs
register_adapter(int64, AsIs)

conexion = psycopg2.connect(
    host=network.ip,
    port=5432,
    database=database.database,
    user=database.user,
    password=database.password
)

# conexion = psycopg2.connect(
#     host="192.168.178.36",
#     port=5432,
#     database='wehka',
#     user='postgres',
#     password='lop34sw@D'
# )


def set(player):
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
    sql = "INSERT INTO jugadores (id_jugador, dni, nombre, apellidos, nick, email, telefono, residencia, talla, "\
          "discapacidades, observaciones) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for cont in range(player.shape[0]):
        data = player.iloc[cont]
        print(data)
        print(cont)
        print(player.shape[0])
        cursor.execute(sql, (data['id_jugador'], data['dni'], data['nombre'], data['apellidos'], data['nick'],
                             data['email'], data['telefono'], data['residencia'], data['talla'], data['discapacidades'],
                             data['observaciones']))
        conexion.commit()

    cursor.close()
    conexion.close()

    return {"label": 'It done'}

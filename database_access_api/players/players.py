# Access to our how Library
# todo: Look for an alternative import to won't see this error.
import pandas as pd
from utils import database, network

# Access to the PostgreSQL database
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


def _locate_id(id):
    '''
    Look for possible IDs that start with the same letters. After we will count how many possible duplicates to sum one
    and add in the three-number format to the ID.
    :param id: The letters of the ID, from the name and surname.
    :return: The number of possible duplicates.
    '''
    sql = "select id_jugador from jugadores where id_jugador LIKE '{}%'".format(id)
    # Connect to the database
    cursor = connection.cursor()
    cursor.execute(sql)
    cuantos = cursor.rowcount
    cursor.close()
    return cuantos


def _new_id(nombre, apellidos):
    '''
    Based in the name and the surname, and looking for posible repetition in the database
    :param nombre:
    :param apellidos:
    :return: A string in which the letters are the first letter of each name and surname, and in addition a number to be
     sure that we don't have duplicate IDs
    '''
    new_id = ''
    for name in nombre.split(' '):
        new_id += name[:1]
    for surname in apellidos.split(' '):
        new_id += surname[:1]
    new_id += f'{_locate_id(new_id) + 1:03d}'
    return new_id


def _invalid_data(**kwargs):
    '''
    We evaluate if the fields shared in the arguments would be unique data into the database.
    :param kwargs: Fields that we will evaluate.
    :return: List of fields with values contained into the database. Null if the data is new.
    '''
    cursor = connection.cursor()
    return_text = ''
    for i in kwargs.items():
        sql = f"select {i[0]} from jugadores where {i[0]} LIKE '{i[1]}'"
        cursor.execute(sql)
        if cursor.rowcount > 0:
            return_text += f'{i[0]}, '
    cursor.close()
    return return_text[:-2]


def add(player):
    '''
    We add the data of the player in to the database.
    In this case only one player.
    This is a first approach, I will need to define the function to build the ID
    :param player: DataFrame with the data of the player.
    :return: none.
    '''

    # Access to the database
    cursor = connection.cursor()
    # Define SQL to insert the data.
    sql = "INSERT INTO jugadores (id_jugador, dni, nombre, apellidos, nick, email, telefono, residencia, talla, "\
          "discapacidades, observaciones) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for cont in range(player.shape[0]):
        data = player.iloc[cont]
        # Build the new_id.
        new_id = _new_id(data['nombre'], data['apellidos'])
        # To ensure we don't have problems with the spelling of the email, we lower it.
        data['email'] = data['email'].lower().copy()
        invalid_data_text = _invalid_data(dni=data['dni'], email=data['email'], telefono=data['telefono'])
        if pd.isnull(invalid_data_text):
            cursor.execute(sql, (new_id, data['dni'], data['nombre'], data['apellidos'], data['nick'],
                                 data['email'], data['telefono'], data['residencia'], data['talla'],
                                 data['discapacidades'], data['observaciones']))
            connection.commit()
            exit_text = {"label": 'It done'}
        else:
            exit_text = {"label": f'Los campos {invalid_data_text} tienen valores previamente almacenados.'}

    return exit_text


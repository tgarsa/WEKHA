# The necessary imports
from utils import network, time
# Access to the Postgres database
import psycopg2
from numpy import int64
# from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(int64, psycopg2.extensions.AsIs)

# TODO: Move to an .env file.
# The connexion parameters
database = 'wehka'
user = 'postgres'
password = 'lop34sw@D'


def add(data, table):
    '''
    We saved the data. Don't do anymore.
    :param cursor: The cursor to access to the database
    :param data: The dataframe with the whole of the data
    :return: Verification text.
    '''

    # Add the connection
    connection = psycopg2.connect(
        host=network.ip,
        port=network.port,
        database=database,
        user=user,
        password=password
    )
    # Connect to the database
    cursor = connection.cursor()

    # SQL to write into treh table
    # List Comprehension approach
    sql = f"INSERT INTO {table} ("
    sql += (', ').join(x for x in data.index)
    sql += ") values ("
    sql += (',').join('%s' for x in data.index)
    sql += ")"

    data_sec = tuple([f"{data[x]}" for x in data.index])

    cursor.execute(sql, data_sec)
    connection.commit()
    cursor.close()
    connection.close()

    return {'label': 'Done it'}


def get(data, table):
    '''
        Download the data of a sede looking for the features passed in the KWARGS.
        :param data: Set of features that we will use to download the data.
        :return: The data of a player.
        '''

    # Add the connection
    connection = psycopg2.connect(
        host=network.ip,
        port=network.port,
        database=database,
        user=user,
        password=password
    )
    # Connect to the database
    cursor = connection.cursor()
    # Start to build the SQL
    sql = f"select * from {table} where"

    for count, column in enumerate(data.columns):
        if count > 0:
            sql += ' and'
        else:
            sql += f" {column} = '{data.iloc[0][column]}'"

    cursor.execute(sql)
    # Download the data
    data = cursor.fetchall()
    # Close the connection
    cursor.close()
    connection.close()

    return data


def update(data, table, id):
    '''
    Here, we update the data's sede
    :param data: Data tu update, + ID
    :param table: Table to update
    :return: Explanatory text.
    '''
    # Add the connection
    connection = psycopg2.connect(
        host=network.ip,
        port=network.port,
        database=database,
        user=user,
        password=password
    )
    # Connect to the database
    cursor = connection.cursor()

    # Working with the data
    id_jugador = data[id]
    data.drop(id, inplace=True)

    # Building the sql to update the data in the Silver Layer.
    sql = f'UPDATE {table} SET'

    for count, column in enumerate(data.index):
        if count > 0:
            sql += ','
        sql += f" {column} = '{data[column]}'"
    sql += f" WHERE {id} = '{id_jugador}'"
    # Execute SQL
    cursor.execute(sql)
    connection.commit()
    # Close the connection
    cursor.close()
    connection.close()
    return {'label': 'Done It'}

